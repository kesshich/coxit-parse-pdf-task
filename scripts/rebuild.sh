#!/bin/bash
set -e

# Force a full rebuild (no layer cache) and restart all services
docker compose down
docker compose build --no-cache
docker compose up -d
docker compose logs -f
