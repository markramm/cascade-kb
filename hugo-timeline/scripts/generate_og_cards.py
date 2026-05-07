#!/usr/bin/env python3
"""Generate Open Graph card PNGs (1200x630) for Capture Cascade Ledger events.

Reads /Users/markr/cascade-kb/cascade-timeline/*.md (Pyrite KB) — the same
source as scripts/generate_content.py — and emits one PNG per event at
static/og/event/<slug>.png. The slug logic mirrors generate_content.write_event
so that Hugo's baseof.html `fileExists` check picks them up.

Defaults to the 400 most-recent events; use --all for the full corpus, --force
to regenerate existing PNGs.
"""
from __future__ import annotations

import argparse
import io
import os
import random
import re
import sys
import time
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ---------------------------------------------------------------------------
# Paths

ROOT = Path(__file__).resolve().parents[1]      # hugo-timeline/
KB = ROOT.parent / "cascade-timeline"
OG_DIR = ROOT / "static" / "og" / "event"
FONT_CACHE = Path(__file__).resolve().parent / ".fonts"

# ---------------------------------------------------------------------------
# Visual design tokens

W, H = 1200, 630

PARCHMENT = (243, 239, 230)        # #f3efe6
PARCHMENT_EDGE = (235, 229, 214)   # #ebe5d6
INK = (28, 26, 23)                 # #1c1a17
INK_3 = (94, 86, 74)               # #5e564a
OXBLOOD = (122, 31, 31)            # #7a1f1f
GILT = (176, 136, 51)              # #b08833
MOSS = (74, 92, 42)                # #4a5c2a
SLATE_BLUE = (42, 74, 92)          # #2a4a5c
DEEP_OXBLOOD = (79, 19, 19)        # #4f1313

LANE_COLORS = {
    "finance":     (122, 31, 31),   # #7a1f1f
    "democracy":   (74, 92, 42),    # #4a5c2a
    "corruption":  (176, 136, 51),  # #b08833
    "labor":       (42, 74, 92),    # #2a4a5c
    "extraction":  (92, 42, 74),    # #5c2a4a
    "other":       (74, 67, 56),    # #4a4338
}

STATUS_COLORS = {
    "confirmed": MOSS,
    "reported":  SLATE_BLUE,
    "alleged":   OXBLOOD,
    "disputed":  DEEP_OXBLOOD,
}

# Google Fonts URLs — single-style TTFs we can embed.
FONT_URLS = {
    "serif": "https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/CormorantGaramond%5Bwght%5D.ttf",
    "serif_italic": "https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/CormorantGaramond-Italic%5Bwght%5D.ttf",
    "mono": "https://raw.githubusercontent.com/google/fonts/main/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
}

# ---------------------------------------------------------------------------
# Slug logic — must mirror generate_content.write_event exactly.

def event_slug(ev: dict) -> str:
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


# ---------------------------------------------------------------------------
# Font loading

def fetch_font(name: str, url: str) -> Path | None:
    FONT_CACHE.mkdir(parents=True, exist_ok=True)
    target = FONT_CACHE / f"{name}.ttf"
    if target.exists() and target.stat().st_size > 1024:
        return target
    if not HAS_REQUESTS:
        return None
    try:
        r = requests.get(url, timeout=20)
        if r.status_code == 200 and len(r.content) > 1024:
            target.write_bytes(r.content)
            return target
    except Exception as e:
        print(f"  font fetch failed for {name}: {e}", file=sys.stderr)
    return None


def system_fallback(kind: str) -> Path | None:
    """Return a TTF path that Pillow can read for serif/serif_italic/mono."""
    candidates = {
        "serif": [
            "/System/Library/Fonts/Supplemental/Georgia.ttf",
            "/System/Library/Fonts/NewYork.ttf",
            "/System/Library/Fonts/Times.ttc",
            "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        ],
        "serif_italic": [
            "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
            "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
        ],
        "mono": [
            "/System/Library/Fonts/SFNSMono.ttf",
            "/System/Library/Fonts/Menlo.ttc",
            "/System/Library/Fonts/Courier.ttc",
        ],
    }
    for p in candidates.get(kind, []):
        if Path(p).exists():
            return Path(p)
    return None


class FontBundle:
    def __init__(self) -> None:
        self.serif_path = fetch_font("serif", FONT_URLS["serif"]) or system_fallback("serif")
        self.serif_italic_path = (
            fetch_font("serif_italic", FONT_URLS["serif_italic"])
            or system_fallback("serif_italic")
            or self.serif_path
        )
        self.mono_path = fetch_font("mono", FONT_URLS["mono"]) or system_fallback("mono")

        if not self.serif_path or not self.mono_path:
            print("  WARN: missing font files; using PIL default", file=sys.stderr)

        self._cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}

    def _load(self, path: Path | None, size: int) -> ImageFont.FreeTypeFont:
        if path is None:
            return ImageFont.load_default()
        key = (str(path), size)
        if key not in self._cache:
            try:
                self._cache[key] = ImageFont.truetype(str(path), size)
            except Exception:
                self._cache[key] = ImageFont.load_default()
        return self._cache[key]

    def serif(self, size: int) -> ImageFont.FreeTypeFont:
        return self._load(self.serif_path, size)

    def serif_italic(self, size: int) -> ImageFont.FreeTypeFont:
        return self._load(self.serif_italic_path, size)

    def mono(self, size: int) -> ImageFont.FreeTypeFont:
        return self._load(self.mono_path, size)


# ---------------------------------------------------------------------------
# Drawing helpers

def text_width(draw: ImageDraw.ImageDraw, text: str, font) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def text_height(draw: ImageDraw.ImageDraw, text: str, font) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[3] - bbox[1]


def wrap_to_width(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    cur = words[0]
    for w in words[1:]:
        test = cur + " " + w
        if text_width(draw, test, font) <= max_width:
            cur = test
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def fit_title(draw: ImageDraw.ImageDraw, fonts: FontBundle, title: str,
              max_width: int, max_lines: int) -> tuple[list[str], ImageFont.FreeTypeFont]:
    """Try shrinking from 70 -> 36 to fit title in max_lines."""
    sizes = [70, 64, 58, 52, 46, 40, 36]
    final_lines: list[str] = []
    final_font = fonts.serif(sizes[-1])
    for size in sizes:
        font = fonts.serif(size)
        lines = wrap_to_width(draw, title, font, max_width)
        if len(lines) <= max_lines:
            return lines, font
        final_lines = lines
        final_font = font
    # Last resort — truncate.
    if len(final_lines) > max_lines:
        kept = final_lines[:max_lines]
        last = kept[-1]
        # Append ellipsis, trimming words until it fits
        while text_width(draw, last + "…", final_font) > max_width and " " in last:
            last = last.rsplit(" ", 1)[0]
        kept[-1] = last + "…"
        final_lines = kept
    return final_lines, final_font


def truncate_to_chars(s: str, n: int) -> str:
    if len(s) <= n:
        return s
    return s[: n - 1].rstrip() + "…"


# ---------------------------------------------------------------------------
# Background / texture

def make_background() -> Image.Image:
    img = Image.new("RGB", (W, H), PARCHMENT)
    # Vertical gradient toward parchment edge near the bottom.
    if HAS_NUMPY:
        arr = np.array(img, dtype=np.int16)
        gradient = np.linspace(0, 1, H).reshape(H, 1, 1)
        edge = np.array(PARCHMENT_EDGE, dtype=np.int16).reshape(1, 1, 3)
        base = np.array(PARCHMENT, dtype=np.int16).reshape(1, 1, 3)
        arr = (base * (1 - gradient) + edge * gradient).astype(np.int16)
        # Subtle noise texture.
        noise = np.random.normal(0, 4, (H, W, 1)).astype(np.int16)
        arr = arr + noise
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        img = Image.fromarray(arr, "RGB")
    else:
        # Light dot texture.
        draw = ImageDraw.Draw(img, "RGBA")
        rng = random.Random(7)
        for _ in range(2500):
            x = rng.randint(0, W - 1)
            y = rng.randint(0, H - 1)
            a = rng.randint(8, 24)
            draw.point((x, y), fill=(140, 130, 110, a))
    return img


# ---------------------------------------------------------------------------
# Lane mapping

def lane_key(raw: str) -> str:
    s = (raw or "").lower()
    if "financial" in s or "finance" in s:
        return "finance"
    if "democratic" in s or "democracy" in s:
        return "democracy"
    if "corruption" in s:
        return "corruption"
    if "labor" in s:
        return "labor"
    if "extraction" in s or "extractive" in s:
        return "extraction"
    return "other"


# ---------------------------------------------------------------------------
# Card composition

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def fmt_date(date_val) -> str:
    s = str(date_val or "")
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", s)
    if not m:
        return s
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if 1 <= mo <= 12:
        return f"{MONTHS[mo - 1]} {d}, {y}"
    return s


def render_card(ev: dict, fonts: FontBundle) -> Image.Image:
    img = make_background()
    draw = ImageDraw.Draw(img, "RGBA")

    pad_x = 80
    pad_top = 56
    pad_bottom = 60
    inner_w = W - 2 * pad_x

    # ---- Top eyebrow ----
    eyebrow = "THE CASCADE LEDGER  ·  CAPTURE CASCADE TIMELINE"
    eyebrow_font = fonts.mono(18)
    draw.text((pad_x, pad_top), eyebrow, font=eyebrow_font, fill=OXBLOOD)
    eb_w = text_width(draw, eyebrow, eyebrow_font)
    rule_y = pad_top + 12
    draw.line(
        [(pad_x + eb_w + 24, rule_y), (W - pad_x, rule_y)],
        fill=GILT, width=1
    )

    # ---- Title block ----
    title_top = pad_top + 78
    title = ev.get("title") or "Untitled event"
    title = truncate_to_chars(title, 320)
    lines, title_font = fit_title(draw, fonts, title, inner_w, max_lines=4)
    line_h = title_font.size + 8
    y = title_top
    for ln in lines:
        draw.text((pad_x, y), ln, font=title_font, fill=INK)
        y += line_h

    # ---- Gilt rule under title ----
    y += 14
    rule_x_end = pad_x + 220
    draw.line([(pad_x, y), (rule_x_end, y)], fill=GILT, width=2)
    y += 24

    # ---- Date ----
    date_str = fmt_date(ev.get("date"))
    date_font = fonts.mono(22)
    draw.text((pad_x, y), date_str, font=date_font, fill=OXBLOOD)
    y += date_font.size + 22

    # ---- Actors ----
    actors = [a for a in (ev.get("actors") or []) if a]
    if actors:
        top_three = actors[:3]
        actor_text = "  ·  ".join(top_three)
        if len(actors) > 3:
            actor_text += f"   +{len(actors) - 3} more"
        actor_text = truncate_to_chars(actor_text, 80)
        actor_font = fonts.serif_italic(24)
        draw.text((pad_x, y), actor_text, font=actor_font, fill=INK_3)
        y += actor_font.size + 24

    # ---- Lane chips ----
    lanes = ev.get("capture_lanes") or []
    if lanes:
        chip_y = y
        chip_x = pad_x
        chip_font = fonts.mono(18)
        seen = set()
        rendered = 0
        for lane in lanes:
            key = lane_key(str(lane))
            label = key  # short, lowercase
            if label in seen:
                continue
            seen.add(label)
            color = LANE_COLORS.get(key, LANE_COLORS["other"])
            # Filled square
            sq = 16
            sq_y = chip_y + 4
            draw.rectangle([chip_x, sq_y, chip_x + sq, sq_y + sq], fill=color)
            chip_x += sq + 8
            draw.text((chip_x, chip_y), label, font=chip_font, fill=INK)
            chip_x += text_width(draw, label, chip_font) + 28
            rendered += 1
            if rendered >= 5 or chip_x > W - pad_x - 100:
                break

    # ---- Bottom bar ----
    bar_y = H - pad_bottom - 18
    draw.line([(pad_x, bar_y), (W - pad_x, bar_y)], fill=PARCHMENT_EDGE, width=1)
    foot_y = bar_y + 16
    domain_font = fonts.mono(18)
    draw.text((pad_x, foot_y), "capturecascade.org",
              font=domain_font, fill=INK_3)

    # Status + importance, right aligned
    status = (ev.get("status") or "").lower().strip()
    importance = ev.get("importance")
    bits: list[tuple[str, tuple[int, int, int]]] = []
    if status:
        bits.append((status, STATUS_COLORS.get(status, INK_3)))
    if importance is not None:
        try:
            imp = int(importance)
            bits.append((f"{imp}/10", INK_3))
        except (ValueError, TypeError):
            pass
    if bits:
        # Render right to left.
        right_x = W - pad_x
        # Compose total
        sep_w = text_width(draw, "  ·  ", domain_font)
        # Place from rightmost backwards
        cursor = right_x
        for i, (txt, color) in enumerate(reversed(bits)):
            tw = text_width(draw, txt, domain_font)
            cursor -= tw
            draw.text((cursor, foot_y), txt, font=domain_font, fill=color)
            if i < len(bits) - 1:
                cursor -= sep_w
                draw.text((cursor, foot_y), "  ·  ", font=domain_font, fill=INK_3)

    return img


# ---------------------------------------------------------------------------
# Main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true",
                    help="Render every event (default: 400 most recent).")
    ap.add_argument("--limit", type=int, default=400,
                    help="Number of most-recent events to render (ignored with --all).")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite existing PNGs.")
    args = ap.parse_args()

    OG_DIR.mkdir(parents=True, exist_ok=True)

    # Load events.
    events: list[dict] = []
    for p in sorted(KB.glob("*.md")):
        if p.name.startswith("_"):
            continue
        ev = parse_kb_event(p)
        if ev:
            events.append(ev)
    print(f"Loaded {len(events)} events from {KB}")

    # Sort by date descending.
    def date_key(ev: dict) -> str:
        return str(ev.get("date") or "")
    events.sort(key=date_key, reverse=True)

    if not args.all:
        events = events[: args.limit]
    print(f"Rendering {len(events)} events "
          f"({'full corpus' if args.all else f'most-recent {args.limit}'})")

    fonts = FontBundle()
    print(f"  serif: {fonts.serif_path}")
    print(f"  serif italic: {fonts.serif_italic_path}")
    print(f"  mono:  {fonts.mono_path}")

    generated = 0
    skipped = 0
    errors = 0
    t0 = time.time()
    sample_path: Path | None = None

    for ev in events:
        slug = event_slug(ev)
        out_path = OG_DIR / f"{slug}.png"
        if out_path.exists() and not args.force:
            skipped += 1
            continue
        try:
            img = render_card(ev, fonts)
            img.save(out_path, "PNG", optimize=True)
            generated += 1
            if sample_path is None:
                sample_path = out_path
        except Exception as e:
            errors += 1
            print(f"  ERROR {slug}: {e}", file=sys.stderr)

    elapsed = time.time() - t0
    print(f"\nGenerated {generated} PNGs · skipped {skipped} existing · errors {errors}")
    print(f"Elapsed: {elapsed:.1f}s")
    if sample_path:
        with Image.open(sample_path) as im:
            print(f"Sample {sample_path.name}: {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()
