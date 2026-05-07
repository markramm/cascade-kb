#!/usr/bin/env bash
# Build the Capture Cascade Timeline site.
# Usage:
#   ./build.sh                # full content + Hugo build → ../public-timeline/
#   ./build.sh serve          # full content + dev server on :1313
#   ./build.sh redirects      # regenerate the legacy → new redirect map only
#   ./build.sh og             # regenerate the 400 most-recent OG card PNGs
#   ./build.sh og --all       # regenerate all OG card PNGs (slow, ~20 min)
set -euo pipefail
cd "$(dirname "$0")"

case "${1:-}" in
  redirects)
    echo "→ Generating redirect map from legacy capturecascade.org URLs…"
    python3 scripts/generate_redirects.py
    exit 0
    ;;
  og)
    shift
    echo "→ Generating OG card PNGs…"
    python3 scripts/generate_og_cards.py "$@"
    exit 0
    ;;
esac

echo "→ Generating Hugo content from Pyrite KB…"
python3 scripts/generate_content.py

# Refresh redirects if old sitemap is reachable, otherwise skip silently.
if curl -sf -o /dev/null --max-time 10 https://capturecascade.org/site/sitemap.xml; then
  echo "→ Refreshing legacy redirect map…"
  python3 scripts/generate_redirects.py
else
  echo "  (skipping redirect refresh — old sitemap unreachable)"
fi

if [[ "${1:-}" == "serve" ]]; then
  echo "→ Serving on http://localhost:1313"
  hugo serve --bind 0.0.0.0 --port 1313 --buildDrafts --disableFastRender
else
  echo "→ Building static site…"
  # Note: --minify is NOT passed because it suppresses custom-format output
  # (sitemap-events.xml, etc.). Hugo's HTML output is already tight enough.
  hugo --gc
  echo "✓ Output written to ../public-timeline/"
fi
