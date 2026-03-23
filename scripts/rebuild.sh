#!/bin/bash
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Force a full rebuild of the deps image first (slow – reinstalls everything)
echo ">>> Rebuilding deps image (no cache)..."
docker build --no-cache \
  -f "$ROOT/backend/docker/backend.deps.dockerfile" \
  -t pdf-parser-backend-deps:latest \
  "$ROOT"

# Now rebuild the app image and restart all services
echo ">>> Rebuilding app and restarting services..."
docker compose -f "$ROOT/docker-compose.yml" down
docker compose -f "$ROOT/docker-compose.yml" build --no-cache
docker compose -f "$ROOT/docker-compose.yml" up -d
docker compose -f "$ROOT/docker-compose.yml" logs -f
