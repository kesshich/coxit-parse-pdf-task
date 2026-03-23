#!/bin/bash
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Build the heavy deps image only when it is missing locally.
# Re-run rebuild.sh if you change pyproject.toml or system packages.
if ! docker image inspect pdf-parser-backend-deps:latest &>/dev/null; then
  echo ">>> Deps image not found – building it now (this takes a while the first time)..."
  docker build -f "$ROOT/backend/docker/backend.deps.dockerfile" -t pdf-parser-backend-deps:latest "$ROOT"
fi

# Build app image (fast – just copies source) and start all services
docker compose -f "$ROOT/docker-compose.yml" up --build -d
docker compose -f "$ROOT/docker-compose.yml" logs -f
