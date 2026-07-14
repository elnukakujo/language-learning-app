"""Back up the current schema on container shutdown, so the next start's
RESTORE_LATEST_BACKUP=true (see restore_latest_backup.py) picks up exactly
where this run left off.
"""
import os
import sys
from pathlib import Path

from config import config as app_config
from lapp.services.backup import BackupService


def main() -> int:
    cfg = app_config[os.environ.get("LAPP_ENV", "default")]
    service = BackupService(
        database_url=cfg.SQLALCHEMY_DATABASE_URI,
        schema=cfg.DB_SCHEMA,
        backup_dir=Path(cfg.BACKUP_ROOT),
        max_backups=cfg.MAX_BACKUPS,
    )

    backup = service.create_backup()
    if backup is None:
        print("Shutdown backup failed.")
        return 1

    print(f"Shutdown backup created: {backup.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
