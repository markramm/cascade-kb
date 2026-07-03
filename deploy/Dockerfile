# syntax=docker/dockerfile:1
# =============================================================================
# Cascade Ledger static-site container
#
# Multi-stage build:
#   1. builder  — runs scripts/generate_content.py, scripts/generate_og_cards.py,
#                 scripts/generate_redirects.py, then `hugo` to emit
#                 /build/public-timeline/.
#   2. runtime  — minimal Caddy (alpine) that serves the static files on :8088.
#                 Same port as the old Pyrite container so the demo Caddyfile
#                 reverse_proxy line keeps working unchanged.
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: build
# -----------------------------------------------------------------------------
FROM python:3.13-slim AS builder

# Install Hugo (extended)
ARG HUGO_VERSION=0.151.2
RUN apt-get update && apt-get install -y --no-install-recommends \
        wget ca-certificates git \
    && wget -q "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb" \
        -O /tmp/hugo.deb \
    && dpkg -i /tmp/hugo.deb \
    && rm /tmp/hugo.deb \
    && apt-get purge -y wget \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Python deps for content generators (Pillow + numpy for OG cards)
RUN pip install --no-cache-dir \
        pyyaml \
        Pillow \
        numpy \
        requests

WORKDIR /build

# Copy KB source (cascade-timeline/) and the Hugo project (hugo-timeline/).
# .git/ is included so generate_content.py can derive per-event lastmod from
# git history (used in sitemap-events.xml).
COPY .git/             ./.git/
COPY cascade-timeline/ ./cascade-timeline/
COPY hugo-timeline/    ./hugo-timeline/

WORKDIR /build/hugo-timeline

# Run the build pipeline.
# The cache mount persists generated OG-card PNGs across builds — the generator
# skips existing files by default, so only NEW/changed events regenerate cards
# instead of rebuilding all ~400 every time (~260s → ~seconds on later builds).
# hugo runs in the same RUN, after generation, so it still copies the cards from
# static/og into the published site.
RUN --mount=type=cache,target=/build/hugo-timeline/static/og \
    python3 scripts/generate_content.py \
    && python3 scripts/generate_og_cards.py --limit 400 \
    && (python3 scripts/generate_redirects.py || echo "  (skipping redirects — no network)") \
    && hugo --gc \
    && python3 scripts/validate_sitemap.py

# Output is at /build/public-timeline/

# -----------------------------------------------------------------------------
# Stage 2: runtime — Caddy serving static files
# -----------------------------------------------------------------------------
FROM caddy:2-alpine AS runtime

# Copy built static site
COPY --from=builder /build/public-timeline /srv

# Caddy config
COPY deploy/Caddyfile.container /etc/caddy/Caddyfile

EXPOSE 8088
