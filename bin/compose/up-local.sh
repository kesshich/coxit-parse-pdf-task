#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

docker_compose_file="docker-compose.yml"

echo "Using docker-compose file: $docker_compose_file"

echo "Building and starting local containers..."
docker compose -f "$docker_compose_file" --progress=plain up -d "$@"

echo "Containers started successfully."
echo ""
echo "Running containers:"
docker compose -f "$docker_compose_file" ps

