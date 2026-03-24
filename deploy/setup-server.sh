#!/bin/bash
# Setup cascade-kb on a server that already runs demo.pyrite.wiki
# Assumes: Docker installed, deploy user exists, Caddy running
set -e

echo "=== Cloning cascade-kb ==="
su - deploy -c '
  git clone https://github.com/markramm/cascade-kb.git ~/cascade-kb
'

echo "=== Building cascade container ==="
su - deploy -c '
  cd ~/cascade-kb
  docker compose -f deploy/docker-compose.yml build
'

echo "=== Starting cascade (no Caddy - uses shared Caddy) ==="
su - deploy -c '
  cd ~/cascade-kb
  docker compose -f deploy/docker-compose.yml up -d pyrite
'

echo "=== Waiting for health ==="
su - deploy -c '
  cd ~/cascade-kb
  timeout 120 bash -c "until docker compose -f deploy/docker-compose.yml exec -T pyrite python -c \"import urllib.request; urllib.request.urlopen(\\\"http://localhost:8088/health\\\")\" 2>/dev/null; do sleep 5; done"
'

echo "=== Seeding KB ==="
su - deploy -c '
  cd ~/cascade-kb
  docker compose -f deploy/docker-compose.yml exec -T pyrite bash /app/seed.sh
'

echo ""
echo "=== Setup complete ==="
echo "Add capturecascade.org to the shared Caddy config."
echo "The cascade Pyrite runs on the internal Docker network."
