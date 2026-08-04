#!/bin/sh
set -e

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
