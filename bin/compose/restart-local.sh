#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

docker_compose_file="docker-compose.yml"

echo "Restarting local development containers..."
docker compose -f "$docker_compose_file" restart "$@"

echo "Containers restarted successfully."

