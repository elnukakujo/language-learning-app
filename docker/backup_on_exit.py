"""Back up the current schema on container shutdown, to a fixed filename so
the next start's RESTORE_LATEST_BACKUP=true (see restore_latest_backup.py)
picks up exactly where this run left off - overwritten each shutdown, never
rotated out by cleanup_old_backups() or superseded by a newer scheduled
backup, since it's outside the backup_{schema}_<timestamp>.dump glob.
"""
import os
import sys
from pathlib import Path

from config import config as app_config
from lapp.services.backup import BackupService

EXIT_SAVE_NAME = "exit_save_{schema}.dump"


def main() -> int:
    cfg = app_config[os.environ.get("LAPP_ENV", "default")]
    service = BackupService(
        database_url=cfg.SQLALCHEMY_DATABASE_URI,
        schema=cfg.DB_SCHEMA,
        backup_dir=Path(cfg.BACKUP_ROOT),
        max_backups=cfg.MAX_BACKUPS,
    )

    backup = service.create_backup(name=EXIT_SAVE_NAME.format(schema=cfg.DB_SCHEMA))
    if backup is None:
        print("Shutdown backup failed.")
        return 1

    print(f"Shutdown backup created: {backup.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
