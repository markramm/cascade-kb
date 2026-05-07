#!/usr/bin/env python3
"""Generate URL redirects from the legacy capturecascade.org/site/ URLs to
the new Hugo site at /event/, /actors/, etc.

Outputs:
  - static/_redirects               Netlify / Cloudflare Pages format
  - static/redirects.nginx.conf     nginx `rewrite ... permanent` directives
  - static/redirects.htaccess       Apache RewriteRule directives

Source data:
  - The old sitemap is fetched live from https://capturecascade.org/site/sitemap.xml
  - The new corpus is read from content/event/*.md and the live actors/tags taxonomy
"""
from __future__ import annotations
import os, re, sys, urllib.request
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "static"
CONTENT = ROOT / "content"

OLD_SITEMAP = "https://capturecascade.org/site/sitemap.xml"
OLD_BASE_PATH = "/site/cascade-timeline"   # everything under here gets remapped
OLD_INDEX_PATH = "/site"                    # the section index → home

# Frozen snapshot of the legacy sitemap, captured 2026-05-06 before migration.
# Used as the source of truth for which URLs need redirects — Google has these
# indexed and the live site no longer has them.
LEGACY_FIXTURE = Path(__file__).parent / "fixtures" / "legacy-urls.txt"

# ─────────────────────────────────────────────────────────────────────
# Load old URLs (prefer the frozen fixture; fall back to the live sitemap)
# ─────────────────────────────────────────────────────────────────────

def fetch_old_urls() -> list[str]:
    if LEGACY_FIXTURE.exists():
        print(f"Using legacy URL fixture: {LEGACY_FIXTURE}")
        # The fixture is bare slugs (one per line, no host/scheme). We need
        # full paths for downstream matching. Reconstruct the canonical URL.
        slugs = [s.strip() for s in LEGACY_FIXTURE.read_text().splitlines() if s.strip()]
        urls = [f"https://capturecascade.org{OLD_BASE_PATH}/{s}" for s in slugs]
        print(f"  loaded {len(urls)} URLs")
        return urls
    print(f"Fetching old sitemap: {OLD_SITEMAP}")
    req = urllib.request.Request(OLD_SITEMAP, headers={"User-Agent": "cascade-redirect-builder/1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode("utf-8", errors="replace")
    locs = re.findall(r"<loc>([^<]+)</loc>", body)
    print(f"  found {len(locs)} URLs")
    return locs

# ─────────────────────────────────────────────────────────────────────
# Load new corpus
# ─────────────────────────────────────────────────────────────────────

def load_new_event_slugs() -> set[str]:
    """All slugs we generated under content/event/<slug>.md"""
    out = set()
    for p in (CONTENT / "event").glob("*.md"):
        out.add(p.stem)
    return out

def load_new_actor_slugs() -> set[str]:
    """Read static/data/actors.json (already produced by generate_content.py)"""
    import json
    p = STATIC / "data" / "actors.json"
    if not p.exists():
        print("  WARN: static/data/actors.json missing — run generate_content.py first")
        return set()
    return set(a["slug"] for a in json.loads(p.read_text()))

# ─────────────────────────────────────────────────────────────────────
# Resolver — pick the best new URL for each old path
# ─────────────────────────────────────────────────────────────────────

def normalize(slug: str) -> str:
    """Lowercase, collapse dots/non-alnum, strip punct — matches both old and new conventions loosely."""
    s = slug.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def build_resolver(events: set[str], actors: set[str]):
    """Returns a function: bare_slug -> new_path or None."""
    # Normalize-keyed lookups for fuzzy matches (donald-trump-jr → donald-trump-jr.)
    norm_events = {normalize(s): s for s in events}
    norm_actors = {normalize(s): s for s in actors}
    # Also strip date prefix from events for matching against bare title-slugs
    date_re = re.compile(r"^\d{4}-\d{2}-\d{2}--(.+)$")
    bare_to_event = {}
    for ev in events:
        m = date_re.match(ev)
        if m:
            bare = m.group(1)
            bare_to_event.setdefault(bare, ev)
            bare_to_event.setdefault(normalize(bare), ev)

    def resolve(slug: str) -> str | None:
        slug = slug.strip("/")
        if not slug or slug in {"_about", "_homepage", "about"}:
            return "/"          # special pages → home
        # 1. Exact event slug match
        if slug in events:
            return f"/event/{slug}/"
        # 2. Normalized event slug match (handles punctuation drift)
        n = normalize(slug)
        if n in norm_events:
            return f"/event/{norm_events[n]}/"
        # 3. Title-slug-only event match (no date prefix in old URL)
        if slug in bare_to_event:
            return f"/event/{bare_to_event[slug]}/"
        if n in bare_to_event:
            return f"/event/{bare_to_event[n]}/"
        # 4. Actor slug match
        if slug in actors:
            return f"/actors/{slug}/"
        if n in norm_actors:
            return f"/actors/{norm_actors[n]}/"
        # 5. Fallback: best-effort search
        return None  # caller decides what to do
    return resolve

# ─────────────────────────────────────────────────────────────────────
# Emit redirects
# ─────────────────────────────────────────────────────────────────────

def main():
    old_urls = fetch_old_urls()
    events = load_new_event_slugs()
    actors = load_new_actor_slugs()
    print(f"  new events: {len(events)}")
    print(f"  new actors: {len(actors)}")
    resolve = build_resolver(events, actors)

    redirects: list[tuple[str, str, int]] = []  # (old_path, new_path, status)
    unresolved: list[str] = []

    # Special static redirects
    redirects.append((f"{OLD_BASE_PATH}", "/", 301))
    redirects.append((f"{OLD_BASE_PATH}/", "/", 301))
    redirects.append((OLD_INDEX_PATH, "/", 301))
    redirects.append(("/site/sitemap.xml", "/sitemap.xml", 301))

    # Process every old URL
    for url in old_urls:
        # Extract path portion
        m = re.match(r"https?://[^/]+(/.+)$", url)
        if not m:
            continue
        path = m.group(1).rstrip("/")
        if not path.startswith(OLD_BASE_PATH):
            continue
        # The slug is everything after /site/cascade-timeline/
        slug = path[len(OLD_BASE_PATH):].lstrip("/")
        if not slug:
            continue
        new = resolve(slug)
        if new:
            redirects.append((path, new, 301))
        else:
            # Unresolved — send to filter view as best effort, with the slug as a search hint
            search = slug.replace("-", "+")[:80]
            redirects.append((path, f"/q/?search={search}", 302))   # 302 since this is a guess
            unresolved.append(path)

    # Dedupe (preserve order)
    seen = set()
    deduped = []
    for r in redirects:
        if r[0] in seen: continue
        seen.add(r[0])
        deduped.append(r)
    redirects = deduped

    # Stats
    n_301 = sum(1 for _, _, s in redirects if s == 301)
    n_302 = sum(1 for _, _, s in redirects if s == 302)
    print(f"\n  emitting {len(redirects)} redirects ({n_301} permanent, {n_302} fallback)")
    print(f"  unresolved (sent to /q/?search=...): {len(unresolved)}")

    # Format 1: Netlify / Cloudflare Pages _redirects
    out1 = STATIC / "_redirects"
    out1.parent.mkdir(parents=True, exist_ok=True)
    with out1.open("w") as f:
        f.write("# Generated by scripts/generate_redirects.py\n")
        f.write("# Format: <old-path> <new-path> <status>\n")
        f.write(f"# {len(redirects)} entries · old domain: capturecascade.org/site/\n\n")
        for old, new, status in redirects:
            f.write(f"{old}  {new}  {status}\n")
    print(f"  wrote {out1} ({out1.stat().st_size//1024} KB)")

    # Format 2: nginx
    out2 = STATIC / "redirects.nginx.conf"
    with out2.open("w") as f:
        f.write("# Generated by scripts/generate_redirects.py\n")
        f.write(f"# Include from server block: include redirects.nginx.conf;\n")
        f.write("# Use exact match via map for performance.\n\n")
        f.write("map $request_uri $cascade_redirect {\n")
        f.write("    default \"\";\n")
        for old, new, _ in redirects:
            # Escape for nginx map keys
            old_e = old.replace('"', '\\"')
            new_e = new.replace('"', '\\"')
            f.write(f'    "{old_e}" "{new_e}";\n')
        f.write("}\n\n")
        f.write("# In your server block:\n")
        f.write("# if ($cascade_redirect) { return 301 $cascade_redirect; }\n")
    print(f"  wrote {out2} ({out2.stat().st_size//1024} KB)")

    # Format 3: Apache .htaccess
    out3 = STATIC / "redirects.htaccess"
    with out3.open("w") as f:
        f.write("# Generated by scripts/generate_redirects.py\n")
        f.write("RewriteEngine On\n\n")
        for old, new, status in redirects:
            # Escape regex metas in `old`
            old_re = re.escape(old)
            f.write(f"RewriteRule ^{old_re[1:]}$ {new} [R={status},L]\n")
    print(f"  wrote {out3} ({out3.stat().st_size//1024} KB)")

    # Format 4: Caddy (read by the inner Caddy in the deploy container)
    out4 = STATIC / "redirects.caddy"
    with out4.open("w") as f:
        f.write("# Generated by scripts/generate_redirects.py\n")
        f.write("# Imported by /etc/caddy/Caddyfile via `import /srv/redirects.caddy`\n")
        f.write(f"# {len(redirects)} entries · maps legacy /site/cascade-timeline/* paths\n")
        f.write("# to the new canonical /event/* / /actors/* paths.\n\n")
        # Emit as a single matcher block: matcher per redirect, then redir.
        # Simpler approach: matcher → redir for each, but each pair is 2 lines.
        # Caddy's `redir` accepts a path matcher inline.
        for old, new, status in redirects:
            # Escape any chars meaningful to Caddy (none here — paths are safe ASCII)
            f.write(f"redir {old} {new} {status}\n")
    print(f"  wrote {out4} ({out4.stat().st_size//1024} KB)")

    # Sample output
    print("\nSample redirects:")
    for r in redirects[:5]:
        print(f"  {r[0]}  →  {r[1]}  ({r[2]})")
    print("  ...")
    for r in redirects[-3:]:
        print(f"  {r[0]}  →  {r[1]}  ({r[2]})")

    if unresolved:
        print(f"\nUnresolved samples (sent to /q/?search=…):")
        for u in unresolved[:8]:
            print(f"  {u}")

if __name__ == "__main__":
    main()
