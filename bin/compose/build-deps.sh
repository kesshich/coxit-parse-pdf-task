#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

DEPS_IMAGE="pdf-parser-backend-deps:latest"

echo "Building backend dependencies image: $DEPS_IMAGE"
echo "This may take a few minutes (only needed when pyproject.toml changes)..."

docker build \
  -f backend/docker/backend.deps.dockerfile \
  -t "$DEPS_IMAGE" \
  .

echo ""
echo "Dependencies image built successfully: $DEPS_IMAGE"

