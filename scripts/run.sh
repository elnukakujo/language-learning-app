#!/usr/bin/env bash
# Run the backend and the Next.js client together. All arguments are
# forwarded to `uv run server` (see pyproject.toml [project.scripts]).
# In prod (--env prod or LAPP_ENV=prod), the client is built once and served
# with `next start`; otherwise it runs `next dev`.
set -euo pipefail
cd "$(dirname "$0")/.."

env_name="${LAPP_ENV:-dev}"
args=("$@")
for i in "${!args[@]}"; do
  if [[ "${args[$i]}" == "--env" && -n "${args[$((i+1))]:-}" ]]; then
    env_name="${args[$((i+1))]}"
  fi
done

uv run server "$@" &
server_pid=$!

cleanup() {
  kill "$server_pid" "$client_pid" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

if [[ "$env_name" == "prod" ]]; then
  (cd client && npm run build && npm run start) &
else
  (cd client && npm run dev) &
fi
client_pid=$!

wait
