#!/bin/sh
set -e

uv run python docker/restore_latest_backup.py
uv run python docker/migrate.py

exec "$@"
