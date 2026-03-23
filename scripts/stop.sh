#!/bin/bash
set -e

# Stop and remove containers (keeps MongoDB volume so data is preserved)
docker compose down
