FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre-headless build-essential curl ca-certificates postgresql-client-16 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY wheels/ ./wheels/
RUN uv sync --frozen --no-dev

COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./
COPY docker/entrypoint.sh /entrypoint.sh
COPY docker/restore_latest_backup.py docker/migrate.py docker/backup_on_exit.py ./docker/
RUN chmod +x /entrypoint.sh

ENV LAPP_HOST=0.0.0.0

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uv", "run", "server"]
