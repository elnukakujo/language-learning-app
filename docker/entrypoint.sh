#!/bin/sh
set -e

uv run python docker/restore_latest_backup.py
uv run alembic upgrade head

exec "$@"
