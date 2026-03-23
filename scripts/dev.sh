#!/bin/bash
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Build images and start all services in the background, then stream logs
docker compose -f "$ROOT/docker-compose.yml" up --build -d
docker compose -f "$ROOT/docker-compose.yml" logs -f
