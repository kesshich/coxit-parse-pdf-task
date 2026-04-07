#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

COMPOSE_FILE="docker-compose.yml"
DEPS_IMAGE="pdf-parser-backend-deps:latest"

# ── Ensure deps image exists ───────────────────────────────────────────────
if ! docker image inspect "$DEPS_IMAGE" > /dev/null 2>&1; then
  echo "Deps image '$DEPS_IMAGE' not found — building it first..."
  bash "$(dirname "${BASH_SOURCE[0]}")/build-deps.sh"
else
  echo "Deps image '$DEPS_IMAGE' found, skipping deps build."
fi

# ── Build app image + start all services ──────────────────────────────────
echo ""
echo "Building app image and starting containers..."
docker compose -f "$COMPOSE_FILE" up --build -d "$@"

echo ""
echo "Containers started successfully."
echo ""
echo "Running containers:"
docker compose -f "$COMPOSE_FILE" ps

