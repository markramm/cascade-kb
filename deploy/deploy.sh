#!/usr/bin/env bash
# Deploy the cascade-ledger static site to the VPS.
#
# Run on the VPS as the `deploy` user:
#   cd ~/cascade-kb && bash deploy/deploy.sh
#
# Steps:
#   1. git pull
#   2. docker compose build cascade
#   3. docker compose up -d cascade
#   4. patch the front-end Caddyfile (capturecascade.org block) to point
#      at cascade:8088 instead of deploy-pyrite-1:8088
#   5. reload the front-end Caddy
#   6. (manual) remove the old pyrite container once verified
#
# Flags:
#   --no-interactive   Skip the disk-prune prompt. Used by CI (GitHub Actions
#                      → SSH → this script). Never prunes in this mode — handle
#                      disk cleanup manually when needed.
set -euo pipefail

NO_INTERACTIVE=0
for arg in "$@"; do
  case "$arg" in
    --no-interactive) NO_INTERACTIVE=1 ;;
    *) echo "Unknown flag: $arg" >&2; exit 2 ;;
  esac
done

cd "$(dirname "$0")/.."

echo "──── Cascade Ledger deploy ────────────────────────────────────"

# Record the currently-deployed commit so we can roll back to it if the new
# build never becomes healthy.
PREV_COMMIT="$(git rev-parse HEAD)"
echo "→ current commit (rollback target): ${PREV_COMMIT:0:12}"

echo "→ git pull"
git pull --ff-only

echo ""
echo "→ Free up Docker disk before build"
docker system df

# ALWAYS reclaim build cache before building — this is safe even on the shared
# host (it only removes unused BUILD CACHE, never volumes, tagged images, or
# other services' data). Without this, cache grows unbounded across deploys and
# eventually fills the disk, stalling the build. (A 76 GB cache once left the
# host at 79% full and hung a deploy mid-build.)
echo "  → pruning unused build cache (safe: cache only, no volumes/images)"
docker builder prune -af >/dev/null 2>&1 || true
docker image prune -f  >/dev/null 2>&1 || true   # dangling images only (-f, not -a)

if [ "$NO_INTERACTIVE" = "1" ]; then
  echo "  (--no-interactive: skipping the deeper full-prune prompt)"
else
  # The deeper prune (-a, all unused images) can reclaim more but removes
  # images not tied to a running container — still never volumes. Opt-in only.
  read -p "  Also run 'docker image prune -a' (removes ALL unused images; never volumes)? [y/N] " yn
  if [[ "$yn" =~ ^[Yy]$ ]]; then
    docker image prune -af
  fi
fi

echo ""
echo "→ Build cascade image"
docker compose -f deploy/docker-compose.yml build cascade

echo ""
echo "→ Start cascade container"
docker compose -f deploy/docker-compose.yml up -d cascade

echo ""
echo "→ Wait for healthy"
HEALTHY=0
for i in $(seq 1 30); do
  if docker compose -f deploy/docker-compose.yml ps cascade 2>/dev/null | grep -q "healthy"; then
    echo "  ✓ cascade is healthy"
    HEALTHY=1
    break
  fi
  sleep 2
  echo "  …waiting ($i/30)"
done

# Rollback rail: if the new container never became healthy, do NOT proceed to
# repoint Caddy at it (that would swap live traffic onto a broken container).
# Revert the checkout to the previously-deployed commit, rebuild, and restart
# the last-known-good version, then fail the deploy loudly.
if [ "$HEALTHY" != "1" ]; then
  echo ""
  echo "  ✗ cascade never became healthy — ROLLING BACK to ${PREV_COMMIT:0:12}"
  git reset --hard "$PREV_COMMIT"
  docker compose -f deploy/docker-compose.yml build cascade
  docker compose -f deploy/docker-compose.yml up -d cascade
  for i in $(seq 1 30); do
    if docker compose -f deploy/docker-compose.yml ps cascade 2>/dev/null | grep -q "healthy"; then
      echo "  ✓ rolled back — previous version is healthy again"
      break
    fi
    sleep 2
  done
  echo "  Deploy FAILED and was rolled back. The live Caddy was never repointed,"
  echo "  so the site kept serving the previous container throughout."
  exit 1
fi

echo ""
echo "→ Patch front-end Caddyfile"
CADDY_FILE="/home/deploy/pyrite/deploy/demo/Caddyfile"
if [ ! -f "$CADDY_FILE" ]; then
  echo "  ! Caddyfile not at $CADDY_FILE — skipping. Edit manually and reload caddy."
  exit 0
fi
if grep -q "reverse_proxy cascade:8088" "$CADDY_FILE"; then
  echo "  ✓ Caddyfile already points at cascade:8088 — no change needed"
else
  cp "$CADDY_FILE" "$CADDY_FILE.bak.$(date +%s)"
  # Replace ONLY the capturecascade.org reverse_proxy line, leave others alone
  sed -i 's|reverse_proxy deploy-pyrite-1:8088|reverse_proxy cascade:8088|' "$CADDY_FILE"
  echo "  ✓ Caddyfile patched (backup at $CADDY_FILE.bak.*)"
fi

echo ""
echo "→ Reload front-end Caddy"
docker exec demo-caddy-1 caddy reload --config /etc/caddy/Caddyfile

echo ""
echo "→ Verify (status + real content — a 200 that serves an empty/broken page must still fail)"
sleep 2

VERIFY_FAIL=0

# Status-line checks (fast smoke test)
echo "  Internal: $(curl -sI -H 'Host: capturecascade.org' http://localhost/ | head -1)"
echo "  Public:   $(curl -sI https://capturecascade.org/ | head -1)"
echo "  Redirect: $(curl -sI https://capturecascade.org/site/cascade-timeline/1142-01-01--haudenosaunee-democratic-consensus-model | head -1)"

# Content checks — fetch the actual bytes and assert expected strings are present.
# A Hugo mis-build can return HTTP 200 with an empty or broken body; status codes
# alone don't catch that. These assert the homepage and a known deep event page
# render real content.
#
# NOTE ON pipefail: do NOT use `echo "$X" | grep -q ...` here. Under
# `set -o pipefail`, `grep -q` exits on first match and SIGPIPEs the upstream
# `echo` (exit 141), which pipefail then reports as a pipeline failure — falsely
# failing the check on a page that DID match. Use `grep -c` on a string (reads
# the whole input, no early exit) and compare the count instead.
echo "  → content assertions:"

HOME_BODY="$(curl -s --max-time 20 https://capturecascade.org/ || true)"
HOME_HITS="$(printf '%s' "$HOME_BODY" | grep -ciE 'cascade|timeline|ledger' || true)"
if [ "${HOME_HITS:-0}" -gt 0 ] && [ "${#HOME_BODY}" -gt 2000 ]; then
  echo "    ✓ homepage: real content (${#HOME_BODY} bytes, ${HOME_HITS} keyword hits)"
else
  echo "    ✗ homepage: MISSING content (${#HOME_BODY} bytes, ${HOME_HITS} hits) — build may be broken"
  VERIFY_FAIL=1
fi

# A known deep event page must render its own title/body (proves the event
# render pipeline worked, not just that the homepage exists).
EVENT_URL="https://capturecascade.org/event/2026-01-31--all-50-states-ice-facility-protests/"
EVENT_BODY="$(curl -sL --max-time 20 "$EVENT_URL" || true)"
EVENT_HITS="$(printf '%s' "$EVENT_BODY" | grep -ciE 'ICE|protest|50501|facility|timeline' || true)"
if [ "${EVENT_HITS:-0}" -gt 0 ] && [ "${#EVENT_BODY}" -gt 1500 ]; then
  echo "    ✓ event page: real content (${#EVENT_BODY} bytes, ${EVENT_HITS} keyword hits)"
else
  echo "    ✗ event page: MISSING content (${#EVENT_BODY} bytes, ${EVENT_HITS} hits) — event render may be broken"
  VERIFY_FAIL=1
fi

if [ "$VERIFY_FAIL" = "1" ]; then
  echo ""
  echo "  ✗ CONTENT VERIFICATION FAILED — the site returns 200 but the body is"
  echo "    empty or missing expected content. ROLLING BACK to ${PREV_COMMIT:0:12}."
  git reset --hard "$PREV_COMMIT"
  docker compose -f deploy/docker-compose.yml build cascade
  docker compose -f deploy/docker-compose.yml up -d cascade
  sleep 5
  echo "    Rolled back to the previous version; the front-end Caddy already"
  echo "    points at the same container name, so traffic follows the rollback."
  exit 1
fi

echo ""
echo "──── Done ─────────────────────────────────────────────────────"
echo ""
echo "Manual cleanup once verified (frees ~3 GB):"
echo "  cd ~/cascade-kb"
echo "  docker compose -f deploy/docker-compose.yml stop pyrite || true"
echo "  docker compose -f deploy/docker-compose.yml rm -f pyrite || true"
echo "  docker volume rm deploy_pyrite-data || true"
