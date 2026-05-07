#!/usr/bin/env bash
# First-time setup of cascade-kb on a server that already runs the shared
# pyrite stack (demo.pyrite.wiki, journalists.pyrite.wiki, demo-caddy-1).
#
# Assumes:
#   - Docker + Compose installed
#   - `deploy` user exists with shell access
#   - The shared front-end Caddy container `demo-caddy-1` is running
#   - The `pyrite-shared` Docker network exists
#
# After this runs once, future updates use `deploy/deploy.sh`.
set -euo pipefail

if [ ! -d /home/deploy/cascade-kb ]; then
  echo "=== Cloning cascade-kb ==="
  su - deploy -c '
    git clone https://github.com/markramm/cascade-kb.git ~/cascade-kb
  '
else
  echo "=== Updating existing clone ==="
  su - deploy -c 'cd ~/cascade-kb && git pull --ff-only'
fi

echo ""
echo "=== Building cascade static container ==="
su - deploy -c '
  cd ~/cascade-kb
  docker compose -f deploy/docker-compose.yml build cascade
'

echo ""
echo "=== Starting cascade ==="
su - deploy -c '
  cd ~/cascade-kb
  docker compose -f deploy/docker-compose.yml up -d cascade
'

echo ""
echo "=== Waiting for healthy ==="
for i in $(seq 1 30); do
  if su - deploy -c 'cd ~/cascade-kb && docker compose -f deploy/docker-compose.yml ps cascade' 2>/dev/null | grep -q "healthy"; then
    echo "  ✓ cascade is healthy"
    break
  fi
  sleep 2
done

echo ""
echo "=== Setup complete ==="
echo ""
echo "Next steps:"
echo "  1. Add or patch the capturecascade.org block in the shared Caddyfile"
echo "     at /home/deploy/pyrite/deploy/demo/Caddyfile — see deploy/Caddyfile"
echo "  2. Reload front-end Caddy:"
echo "       docker exec demo-caddy-1 caddy reload --config /etc/caddy/Caddyfile"
echo "  3. Verify: curl -sI https://capturecascade.org/"
echo ""
echo "For ongoing updates, use deploy/deploy.sh (patches Caddyfile automatically)."
