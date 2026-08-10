#!/bin/sh
# Deploy Fluence with Docker Compose.
# Run on PCT after `git pull`.
set -e
cd "$(dirname "$0")"

# Guard: LAPP_PUBLIC_HOST must be set in .env (frontend bakes it at build time;
# a missing/empty value silently produces a build pointed at localhost).
grep -qE '^LAPP_PUBLIC_HOST=.+' .env || {
  echo "ERROR: LAPP_PUBLIC_HOST is not set in .env" >&2
  exit 1
}

git pull --ff-only
docker compose up -d --build --remove-orphans
docker builder prune -af
docker image prune -f
