#!/usr/bin/env python3
"""Generate Hugo content for the Capture Cascade Timeline.

Reads cascade-timeline/*.md (Pyrite KB), emits:
  - content/event/<slug>.md           one per timeline event (with wikilinks resolved)
  - content/year/_index.md            section index
  - content/decade/_index.md          section index
  - data/density.json                 [{year:int, count:int}, ...] for homepage chart
  - data/quality.json                 {warnings, summary} from sanitizer pass
  - static/data/timeline.json         denormalized dataset for /q/ filter
  - static/robots.txt                 with explicit AI-crawler rules

The content uses Hugo type=event so layouts/event/single.html renders it.
We map capture_lanes → Hugo taxonomy "lanes", tags → "tags", actors → "actors".
"""
from __future__ import annotations
import json, os, re, sys, yaml
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]      # hugo-timeline/
KB   = ROOT.parent / "cascade-timeline"
EXP  = ROOT.parent / "export"
DATA = ROOT / "data"
CONTENT = ROOT / "content"
STATIC = ROOT / "static" / "data"

START_YEAR = 1142
END_YEAR   = 2026

def hugo_urlize(s: str) -> str:
    """Mirror Hugo's `urlize` function — lowercase, replace spaces and most
    punctuation with dashes, but PRESERVE dots and other path-safe chars.
    This matches what Hugo emits for /actors/<urlize>/ paths."""
    s = s.lower()
    # Hugo's urlize keeps a-z 0-9 and a small set of safe chars (-._~)
    # Everything else becomes a dash; runs of dashes collapse.
    s = re.sub(r"[^a-z0-9._~]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")

# Backwards-compat alias used by the file slug logic — but for filesystem
# slugs we want the stricter version (no dots, since some filesystems are
# picky and the slug also becomes the file name).
def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

# ─────────────────────────────────────────────────────────────────────
# Slug logic — must mirror the cap rule used by generate_og_cards.py
# ─────────────────────────────────────────────────────────────────────

def make_slug(ev: dict) -> str:
    slug = ev.get("id") or ev["_filename"]
    if len(slug) > 200:
        date_match = re.match(r"^(\d{4}-\d{2}-\d{2}--)", slug)
        if date_match:
            prefix = date_match.group(1)
            slug = prefix + slug[len(prefix):][:180]
        else:
            slug = slug[:200]
        slug = slug.rstrip("-")
    return slug

# ─────────────────────────────────────────────────────────────────────
# Parser
# ─────────────────────────────────────────────────────────────────────

def parse_kb_event(path: Path) -> dict | None:
    txt = path.read_text(encoding="utf-8")
    if not txt.startswith("---"):
        return None
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", txt, re.DOTALL)
    if not m:
        return None
    fm_raw, body = m.group(1), m.group(2)
    try:
        fm = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError:
        return None
    if fm.get("type") != "timeline_event":
        return None
    fm["body"] = body.strip()
    fm["_filename"] = path.stem
    return fm

# ─────────────────────────────────────────────────────────────────────
# Wikilink resolution — [[slug]] → <a> or .needs-entry span
# ─────────────────────────────────────────────────────────────────────

WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]")

def build_slug_index(events: list[dict]) -> dict[str, str]:
    """Map every known event slug AND its un-dated alias to the canonical slug.

    Pyrite wikilinks come in two flavors:
      [[2025-02-14--vance-munich-security-conference-speech]]   ← exact slug
      [[vance-jd]]                                              ← actor/concept alias (no event)

    We index both. Aliases that don't resolve render as `needs-entry`.
    """
    idx: dict[str, str] = {}
    for ev in events:
        slug = make_slug(ev)
        # Canonical slug
        idx[slug] = slug
        # Drop date prefix for alias lookup (`2025-02-14--foo` → `foo`)
        bare = re.sub(r"^\d{4}-\d{2}-\d{2}--", "", slug)
        if bare and bare not in idx:
            idx[bare] = slug
    return idx

def resolve_wikilinks(body: str, slug_idx: dict[str, str]) -> tuple[str, list[str]]:
    """Replace [[target]] with HTML. Return (new_body, list_of_unresolved)."""
    unresolved: list[str] = []

    def repl(m: re.Match) -> str:
        target = m.group(1).strip()
        label  = (m.group(2) or target).strip()
        # Strip any trailing markdown italic/needs-entry markers from the target
        target_clean = re.sub(r"\s*\*[^*]+\*\s*$", "", target).strip()
        # Lookup
        canonical = slug_idx.get(target_clean) or slug_idx.get(target_clean.lower())
        if canonical:
            return f'<a href="/event/{canonical}/" class="wikilink">{label}</a>'
        unresolved.append(target_clean)
        return f'<span class="needs-entry" title="entry not yet written">{label}</span>'

    new = WIKILINK_RE.sub(repl, body)
    # Also clean up trailing " — *needs entry*" annotations adjacent to wikilinks (or anywhere)
    new = re.sub(r"\s*—\s*\*needs entry\*", "", new, flags=re.IGNORECASE)
    return new, unresolved

# ─────────────────────────────────────────────────────────────────────
# Source-data quality sanitizer
# ─────────────────────────────────────────────────────────────────────

def audit_event(ev: dict, slug_idx: dict[str, str]) -> list[dict]:
    """Return a list of issues for a single event. Each issue: {code, msg}."""
    issues: list[dict] = []
    title = (ev.get("title") or "").strip()
    body  = ev.get("body") or ""
    sources = ev.get("sources") or []
    status  = (ev.get("status") or "").lower()

    # 1. Suspicious zeroed-out dollar amounts: "$0B", "$00B", "00 Million"
    if re.search(r"\$0[0-9]?\s*[BMKbmk]\b", title) or re.search(r"\b0[0B]\s*Billion\b", title):
        issues.append({"code": "suspicious-amount",
                       "msg": f"Title contains a likely-corrupted dollar amount: {title!r}"})

    # 2. Lowercase title start (likely truncation or formatting bug)
    if title and title[0].islower():
        issues.append({"code": "lowercase-title",
                       "msg": "Title begins with lowercase letter"})

    # 3. Visible "needs entry" placeholder bleeding into body or title
    for field, txt in (("title", title), ("body", body)):
        if re.search(r"\bneeds\s+entry\b", txt, flags=re.IGNORECASE):
            issues.append({"code": "needs-entry-leak",
                           "msg": f"Visible 'needs entry' placeholder in {field}"})
            break

    # 4. Confirmed status with zero sources
    if status == "confirmed" and not sources:
        issues.append({"code": "confirmed-no-sources",
                       "msg": "Status=confirmed but sources list is empty"})

    # 5. Source missing URL
    for i, s in enumerate(sources):
        if isinstance(s, dict) and not s.get("url"):
            issues.append({"code": "source-no-url",
                           "msg": f"Source #{i+1} has no URL: {s.get('title') or '<no title>'}"})

    # 6. Unresolved wikilinks (computed against slug_idx)
    for m in WIKILINK_RE.finditer(body):
        tgt = re.sub(r"\s*\*[^*]+\*\s*$", "", m.group(1).strip())
        if tgt and tgt not in slug_idx and tgt.lower() not in slug_idx:
            issues.append({"code": "unresolved-wikilink",
                           "msg": f"[[{tgt}]] does not match any event slug or alias"})
            break  # one report per event is enough

    # 7. Empty body (probably ingestion failure)
    if not body.strip():
        issues.append({"code": "empty-body",
                       "msg": "Event body is empty"})

    return issues

# ─────────────────────────────────────────────────────────────────────
# Writers
# ─────────────────────────────────────────────────────────────────────

def write_event(ev: dict, slug_idx: dict[str, str]) -> None:
    slug = make_slug(ev)
    body = ev.get("body") or ""
    body_resolved, _ = resolve_wikilinks(body, slug_idx)
    fm = {
        "title": ev.get("title", "Untitled event"),
        "slug":  slug,
        "type":  "event",
        "date":  ev.get("date"),
        "lastmod": ev.get("lastmod") or ev.get("date"),
        "summary": (body or "").split("\n\n", 1)[0][:280] if body else "",
        "actors": ev.get("actors", []) or [],
        "tags":   ev.get("tags", []) or [],
        "lanes":  ev.get("capture_lanes", []) or [],
        "year":   [str(ev["date"])[:4]] if ev.get("date") else [],   # Hugo: plural=singular ("year")
        "decade": [f"{str(ev['date'])[:3]}0s"] if ev.get("date") else [],
        "importance": ev.get("importance"),
        "status": ev.get("status"),
        "sources": ev.get("sources", []) or [],
        "capture_lanes": ev.get("capture_lanes", []) or [],
        "coverage": ev.get("coverage", []) or [],
    }
    out = CONTENT / "event" / f"{slug}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    yaml_fm = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, default_flow_style=False).strip()
    out.write_text(f"---\n{yaml_fm}\n---\n\n{body_resolved}\n", encoding="utf-8")

def write_term_pages(events: list[dict]) -> None:
    (CONTENT / "year").mkdir(parents=True, exist_ok=True)
    (CONTENT / "decade").mkdir(parents=True, exist_ok=True)
    (CONTENT / "year" / "_index.md").write_text(
        "---\ntitle: \"Years of record\"\nsummary: \"Every year between 1142 and today, with the verified events recorded against it.\"\n---\n", encoding="utf-8"
    )
    (CONTENT / "decade" / "_index.md").write_text(
        "---\ntitle: \"Decades of record\"\nsummary: \"Walk the timeline by decade. Each page lists every verified event in chronological order.\"\n---\n", encoding="utf-8"
    )

def write_density(events: list[dict]) -> None:
    counts: dict[int, int] = defaultdict(int)
    for ev in events:
        if not ev.get("date"): continue
        try:
            y = int(str(ev["date"])[:4])
        except ValueError:
            continue
        if START_YEAR <= y <= END_YEAR:
            counts[y] += 1
    rows = [{"year": y, "count": counts.get(y, 0)} for y in range(START_YEAR, END_YEAR + 1)]
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "density.json").write_text(json.dumps(rows), encoding="utf-8")
    print(f"  density.json: {len(rows)} years, peak {max(counts.values()) if counts else 0}")

def write_filter_dataset(events: list[dict]) -> None:
    STATIC.mkdir(parents=True, exist_ok=True)
    out = []
    for ev in events:
        body = (ev.get("body") or "")[:600]
        out.append({
            "id":      ev.get("id") or ev["_filename"],
            "title":   ev.get("title", ""),
            "date":    str(ev.get("date") or ""),
            "actors":  ev.get("actors") or [],
            "tags":    ev.get("tags") or [],
            "capture_lanes": ev.get("capture_lanes") or [],
            "status":  ev.get("status"),
            "importance": ev.get("importance"),
            "body":    body,
        })
    out.sort(key=lambda e: e.get("date") or "")
    (STATIC / "timeline.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print(f"  timeline.json: {len(out)} events ({(STATIC/'timeline.json').stat().st_size//1024} KB)")

def write_co_actors(events: list[dict]) -> None:
    """For each actor, pre-compute their top-24 co-occurring actors (count desc).

    Output: data/co_actors.json keyed by actor name → list of {name, count}.
    Avoids the O(N²) `merge` loop in the Hugo template.
    """
    co: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for ev in events:
        actors = ev.get("actors") or []
        for a in actors:
            for b in actors:
                if a == b: continue
                co[a][b] += 1
    out: dict[str, dict] = {}
    for actor, partners in co.items():
        ranked = sorted(partners.items(), key=lambda x: (-x[1], x[0]))
        out[actor] = {
            "total": len(partners),
            "top": [{"name": n, "count": c, "slug": hugo_urlize(n)} for n, c in ranked[:24]],
        }
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "co_actors.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print(f"  co_actors.json: {len(out)} actors with co-occurrence data")

def build_lastmod_map(events: list[dict]) -> dict[str, str]:
    """Run a single `git log` pass to get last-commit date for every event
    source file in cascade-timeline/. Returns {slug: ISO8601-date}.

    Falls back to filesystem mtime if git is unavailable (e.g. shallow
    Docker contexts without .git/), and to build time if mtime is also
    suspicious. ISO8601 with timezone, ready for sitemap consumption.
    """
    import subprocess, datetime as _dt
    out: dict[str, str] = {}
    build_now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    cutoff = _dt.datetime(1970, 1, 1, tzinfo=_dt.timezone.utc)

    # Single git invocation listing every file in cascade-timeline/ with its
    # most recent commit timestamp. ~700ms on a 5K-file repo vs. ~30s for
    # 5,000 individual `git log -1` calls.
    git_dir = KB.parent
    git_dates: dict[str, str] = {}
    try:
        # `git log --name-only --format=%cI` walks history once, emitting
        # commit timestamp followed by changed-file paths. We keep the FIRST
        # timestamp seen per file (newest commit wins because `git log`
        # defaults to reverse-chronological).
        proc = subprocess.run(
            ["git", "log", "--name-only", "--format=%cI"],
            cwd=git_dir, capture_output=True, text=True, timeout=120,
        )
        if proc.returncode == 0:
            current_ts = ""
            for line in proc.stdout.splitlines():
                line = line.strip()
                if not line:
                    continue
                if re.match(r"^\d{4}-\d{2}-\d{2}T", line):
                    current_ts = line
                elif current_ts and line.startswith("cascade-timeline/"):
                    rel = line[len("cascade-timeline/"):]
                    git_dates.setdefault(rel, current_ts)   # first = newest
            print(f"  lastmod: collected {len(git_dates)} git timestamps")
        else:
            print(f"  lastmod: git log failed (rc={proc.returncode}), using mtime fallback")
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"  lastmod: git unavailable ({e!s}), using mtime fallback")

    for ev in events:
        slug = make_slug(ev)
        # 1. Prefer git timestamp
        fname = ev["_filename"] + ".md"
        ts = git_dates.get(fname)
        # 2. Fall back to mtime
        if not ts:
            try:
                mtime = (KB / fname).stat().st_mtime
                dt = _dt.datetime.fromtimestamp(mtime, _dt.timezone.utc)
                ts = dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")
            except OSError:
                ts = build_now
        # 3. Validate — Google rejects pre-1970
        try:
            parsed = _dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
            if parsed < cutoff:
                ts = build_now
        except ValueError:
            ts = build_now
        out[slug] = ts

    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "lastmod.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    git_count = sum(1 for s in out.values() if s != build_now)
    print(f"  lastmod.json: {len(out)} entries ({git_count} from git, {len(out)-git_count} build-time fallback)")
    return out

def write_resonance_index(events: list[dict]) -> None:
    """Pre-compute the "on this day" / historical-resonance lookup.

    Index events by (MM-DD) → list of (year, slug, title). For each event, the
    template can then look up "1 year ago today", "5 years ago today", etc.
    without scanning the corpus.

    Output: data/resonance.json keyed by MMDD as 4-digit string ("0214" for Feb 14).
    """
    by_mmdd: dict[str, list[dict]] = defaultdict(list)
    for ev in events:
        d = str(ev.get("date") or "")
        if len(d) < 10: continue
        mmdd = d[5:7] + d[8:10]   # "02-14" → "0214"
        try:
            year = int(d[:4])
        except ValueError:
            continue
        by_mmdd[mmdd].append({
            "year": year,
            "slug": make_slug(ev),
            "title": ev.get("title", "")[:120],
        })
    # Sort each list by year ascending (so we can pick "5 years ago" deterministically)
    for k in by_mmdd:
        by_mmdd[k].sort(key=lambda e: e["year"])
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "resonance.json").write_text(json.dumps(dict(by_mmdd), separators=(",", ":")), encoding="utf-8")
    total = sum(len(v) for v in by_mmdd.values())
    print(f"  resonance.json: {len(by_mmdd)} unique mm-dd buckets, {total} events")

def write_taxonomy_indexes(events: list[dict]) -> None:
    """Emit lightweight {name, count} arrays for the actors/tags index pages
    to lazy-load. Keeps the static HTML page small."""
    STATIC.mkdir(parents=True, exist_ok=True)
    actor_counts: dict[str, int] = defaultdict(int)
    tag_counts: dict[str, int] = defaultdict(int)
    for ev in events:
        for a in ev.get("actors") or []:
            actor_counts[a] += 1
        for t in ev.get("tags") or []:
            tag_counts[t] += 1

    actors = sorted(
        ({"name": k, "count": v, "slug": hugo_urlize(k)} for k, v in actor_counts.items()),
        key=lambda x: (-x["count"], x["name"].lower()),
    )
    tags = sorted(
        ({"name": k, "count": v, "slug": hugo_urlize(k)} for k, v in tag_counts.items()),
        key=lambda x: (-x["count"], x["name"].lower()),
    )
    (STATIC / "actors.json").write_text(json.dumps(actors, separators=(",", ":")), encoding="utf-8")
    (STATIC / "tags.json").write_text(json.dumps(tags, separators=(",", ":")), encoding="utf-8")
    print(f"  actors.json: {len(actors)} entries ({(STATIC/'actors.json').stat().st_size//1024} KB)")
    print(f"  tags.json:   {len(tags)} entries ({(STATIC/'tags.json').stat().st_size//1024} KB)")

def write_quality_report(events: list[dict], slug_idx: dict[str, str]) -> dict:
    """Audit the whole corpus and write a JSON report."""
    warnings: list[dict] = []
    code_counts: dict[str, int] = defaultdict(int)
    for ev in events:
        issues = audit_event(ev, slug_idx)
        if issues:
            warnings.append({
                "id": ev.get("id") or ev["_filename"],
                "title": ev.get("title"),
                "date": str(ev.get("date") or ""),
                "issues": issues,
            })
            for it in issues:
                code_counts[it["code"]] += 1

    summary = {
        "total_events": len(events),
        "events_with_warnings": len(warnings),
        "issue_count_by_code": dict(code_counts),
        "scanned_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "quality.json").write_text(
        json.dumps({"summary": summary, "warnings": warnings}, indent=2),
        encoding="utf-8"
    )
    print(f"  quality.json: {len(warnings)}/{len(events)} events flagged")
    for code, n in sorted(code_counts.items(), key=lambda x: -x[1]):
        print(f"    {n:>5}  {code}")
    return summary

# ─────────────────────────────────────────────────────────────────────
# robots.txt — explicit AI-crawler rules. Goal: maximum LLM ingestion.
# ─────────────────────────────────────────────────────────────────────

ROBOTS_TXT = """\
# The Capture Cascade Timeline — robots policy
#
# This is a public documentary archive published under CC BY-SA 4.0.
# We WANT search engines, AI training crawlers, and LLM retrieval bots to
# index and surface this content. The goal is for "capture cascade",
# specific events, and named actors to be answerable by chatbots and
# search engines worldwide.
#
# Attribution is required by license. We do not block any well-behaved bot.

User-agent: *
Allow: /
Crawl-delay: 1

# Search engines (general)
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: DuckDuckBot
Allow: /

User-agent: Applebot
Allow: /

# AI training & retrieval crawlers — explicitly welcomed
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: cohere-ai
Allow: /

User-agent: Bytespider
Allow: /

User-agent: meta-externalagent
Allow: /

User-agent: Diffbot
Allow: /

# Social unfurlers (so link previews work)
User-agent: Twitterbot
Allow: /

User-agent: facebookexternalhit
Allow: /

User-agent: LinkedInBot
Allow: /

User-agent: Slackbot
Allow: /

User-agent: Discordbot
Allow: /

# Sitemap
Sitemap: https://capturecascade.org/sitemap.xml
"""

def write_robots() -> None:
    (ROOT / "static").mkdir(parents=True, exist_ok=True)
    (ROOT / "static" / "robots.txt").write_text(ROBOTS_TXT, encoding="utf-8")

def write_master_sitemap() -> None:
    """Write a static sitemap-index pointing to the four section fragments
    that Hugo emits via custom output formats. Hugo's built-in sitemap
    output is disabled (hugo.toml [sitemap] disable=true), and Hugo's
    HTML auto-escape mangles the `<?xml ?>` declaration when used through
    Go template engine — so we write this directly here as plain text."""
    base = "https://capturecascade.org/"
    now = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    body = f"""<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>{base}sitemap-events.xml</loc>
    <lastmod>{now}</lastmod>
  </sitemap>
  <sitemap>
    <loc>{base}sitemap-actors.xml</loc>
    <lastmod>{now}</lastmod>
  </sitemap>
  <sitemap>
    <loc>{base}sitemap-tags.xml</loc>
    <lastmod>{now}</lastmod>
  </sitemap>
  <sitemap>
    <loc>{base}sitemap-meta.xml</loc>
    <lastmod>{now}</lastmod>
  </sitemap>
</sitemapindex>
"""
    (ROOT / "static").mkdir(parents=True, exist_ok=True)
    (ROOT / "static" / "sitemap.xml").write_text(body, encoding="utf-8")
    print(f"  sitemap.xml: written ({len(body)} bytes, points at 4 fragments)")

# ─────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────

def main():
    events = []
    for p in sorted(KB.glob("*.md")):
        if p.name.startswith("_"):
            continue
        ev = parse_kb_event(p)
        if ev:
            events.append(ev)
    print(f"Loaded {len(events)} events from {KB}")

    slug_idx = build_slug_index(events)
    print(f"  slug index: {len(slug_idx)} canonical+alias entries")

    # Truncate / clean prior generated content
    evdir = CONTENT / "event"
    if evdir.exists():
        for f in evdir.glob("*.md"):
            f.unlink()
    evdir.mkdir(parents=True, exist_ok=True)

    for ev in events:
        write_event(ev, slug_idx)
    print(f"  wrote {len(events)} event pages (with wikilinks resolved)")

    write_term_pages(events)
    write_density(events)
    write_filter_dataset(events)
    write_taxonomy_indexes(events)
    write_resonance_index(events)
    write_co_actors(events)
    build_lastmod_map(events)
    write_quality_report(events, slug_idx)
    write_robots()
    write_master_sitemap()
    print("Done.")

if __name__ == "__main__":
    main()
