"""Restore the schema's latest backup, if RESTORE_LATEST_BACKUP=true. Run before
alembic upgrade so a restored dump lands before any pending migrations apply."""
import os
import sys
from pathlib import Path

from config import config as app_config
from lapp.services.backup import BackupService


def main() -> int:
    if os.environ.get("RESTORE_LATEST_BACKUP", "").lower() not in ("1", "true", "yes"):
        print("RESTORE_LATEST_BACKUP not set, skipping restore.")
        return 0

    cfg = app_config[os.environ.get("LAPP_ENV", "default")]
    service = BackupService(
        database_url=cfg.SQLALCHEMY_DATABASE_URI,
        schema=cfg.DB_SCHEMA,
        backup_dir=Path(cfg.BACKUP_ROOT),
        max_backups=cfg.MAX_BACKUPS,
    )

    latest = service.get_latest_backup()
    if latest is None:
        print("No backup found, skipping restore.")
        return 0

    print(f"Restoring latest backup: {latest.name}")
    return 0 if service.restore_backup(latest) else 1


if __name__ == "__main__":
    sys.exit(main())
