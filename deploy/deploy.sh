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
set -euo pipefail

cd "$(dirname "$0")/.."

echo "──── Cascade Ledger deploy ────────────────────────────────────"

echo "→ git pull"
git pull --ff-only

echo ""
echo "→ Free up Docker disk before build"
docker system df
read -p "  Run 'docker system prune -a' first? (recommended; frees old Pyrite layers) [y/N] " yn
if [[ "$yn" =~ ^[Yy]$ ]]; then
  docker system prune -af --volumes
fi

echo ""
echo "→ Build cascade image"
docker compose -f deploy/docker-compose.yml build cascade

echo ""
echo "→ Start cascade container"
docker compose -f deploy/docker-compose.yml up -d cascade

echo ""
echo "→ Wait for healthy"
for i in $(seq 1 30); do
  if docker compose -f deploy/docker-compose.yml ps cascade 2>/dev/null | grep -q "healthy"; then
    echo "  ✓ cascade is healthy"
    break
  fi
  sleep 2
  echo "  …waiting ($i/30)"
done

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
echo "→ Verify"
sleep 2
echo "  Internal: $(curl -sI -H 'Host: capturecascade.org' http://localhost/  | head -1)"
echo "  Public:   $(curl -sI https://capturecascade.org/ | head -1)"
echo "  Redirect: $(curl -sI https://capturecascade.org/site/cascade-timeline/1142-01-01--haudenosaunee-democratic-consensus-model | head -1)"

echo ""
echo "──── Done ─────────────────────────────────────────────────────"
echo ""
echo "Manual cleanup once verified (frees ~3 GB):"
echo "  cd ~/cascade-kb"
echo "  docker compose -f deploy/docker-compose.yml stop pyrite || true"
echo "  docker compose -f deploy/docker-compose.yml rm -f pyrite || true"
echo "  docker volume rm deploy_pyrite-data || true"
