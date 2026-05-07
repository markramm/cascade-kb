#!/usr/bin/env python3
"""Sitemap sanity check — fails the build if URLs would trip Google's parser.

Google Search Console silently rejects sitemaps when individual URLs contain
embedded slashes inside what should be a single slug segment (e.g. an
unescaped `/` in a taxonomy term name). The XML is structurally valid and
the URLs return 200, but GSC reports "Invalid date / 698 instances" or
similar opaque errors and refuses to index the affected sections.

Run this after `hugo --gc`. Exits non-zero if any sitemap URL contains:
  - more than the expected number of path segments for its section
  - a `//` sequence (empty segment)
  - a `/-` or `-/` boundary (slash adjacent to dash)

Sections and their expected path-segment count (after the host):
  /                              0
  /q/, /timelines/, /about/      1
  /actors/<slug>/                2
  /lanes/<slug>/                 2
  /tags/<slug>/                  2
  /year/<slug>/                  2
  /decade/<slug>/                2
  /event/<slug>/                 2
  /timelines/<slug>/             2
  /about/<page>/                 2

Anything deeper means a slug contained an unescaped `/`.
"""

import sys
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT.parent / "public-timeline"

ALLOWED_DEEP_PREFIXES = (
    "/about/",  # /about/methodology/, /about/sources/, etc.
)

PROBLEM_PATTERNS = [
    (re.compile(r"//"), "empty path segment"),
    (re.compile(r"/-"), "slug starts with dash"),
    (re.compile(r"-/"), "slug ends with dash"),
]


def check_url(url: str) -> list[str]:
    issues = []
    p = urlparse(url)
    path = p.path
    for pat, msg in PROBLEM_PATTERNS:
        if pat.search(path):
            issues.append(f"{msg}: {path}")
    # Path depth check — strip leading/trailing slash, count segments
    segs = [s for s in path.strip("/").split("/") if s]
    is_about = any(path.startswith(pfx) for pfx in ALLOWED_DEEP_PREFIXES)
    if not is_about and len(segs) > 2:
        issues.append(f"too many path segments ({len(segs)}): {path}")
    return issues


def main() -> int:
    sitemaps = list(PUBLIC.glob("sitemap-*.xml"))
    if not sitemaps:
        print(f"[validate_sitemap] no sitemap-*.xml under {PUBLIC}", file=sys.stderr)
        return 1
    total = 0
    bad = 0
    for sm in sorted(sitemaps):
        urls = re.findall(r"<loc>([^<]+)</loc>", sm.read_text(encoding="utf-8"))
        for u in urls:
            total += 1
            for issue in check_url(u):
                bad += 1
                print(f"[validate_sitemap] {sm.name}: {issue}", file=sys.stderr)
    print(f"[validate_sitemap] checked {total} URLs across {len(sitemaps)} sitemaps; {bad} issues")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
