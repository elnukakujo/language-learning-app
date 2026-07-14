"""Bring the schema up to date via DatabaseManager.run_migrations(), which
bootstraps brand-new databases with create_all()+stamp instead of replaying
history against tables that don't exist yet (see database.py:run_migrations).
"""
import os
import sys

import sqlalchemy

from config import config as app_config
from lapp.core.database import DatabaseManager


def main() -> int:
    cfg = app_config[os.environ.get("LAPP_ENV", "default")]
    manager = DatabaseManager(cfg.SQLALCHEMY_DATABASE_URI)

    db_schema = getattr(cfg, "DB_SCHEMA", None)
    if db_schema:
        with manager.engine.connect() as connection:
            connection.execute(sqlalchemy.text(f'CREATE SCHEMA IF NOT EXISTS "{db_schema}"'))
            connection.commit()

    manager.run_migrations()
    return 0


if __name__ == "__main__":
    sys.exit(main())
