#!/bin/sh
set -e

# Fail fast if the storage mount is missing (e.g. NAS not mounted on prod).
test -d /app/backups || { echo "FATAL: /app/backups not mounted (NAS down?)"; exit 1; }

uv run --frozen --no-dev python docker/restore_latest_backup.py
uv run --frozen --no-dev python docker/migrate.py

"$@" &
child=$!

term_handler() {
    uv run --frozen --no-dev python docker/backup_on_exit.py
    kill -TERM "$child" 2>/dev/null
    wait "$child"
}
trap term_handler TERM INT

wait "$child"
