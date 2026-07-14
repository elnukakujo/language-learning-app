import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from sqlalchemy.engine import make_url

logger = logging.getLogger(__name__)

class BackupService:
    """
    Service for managing database backups via pg_dump/pg_restore, scoped to
    one Postgres schema (one config: dev/test/prod).

    This service handles:
    - Creating database backups
    - Restoring from backups
    - Cleanup of old backups
    - Backup file management

    Note: This is a pure service class without scheduling logic.
    Scheduling is handled by APScheduler in tasks/scheduled.py
    """

    def __init__(
        self,
        database_url: str,
        schema: str,
        backup_dir: Path,
        max_backups: int = 10
    ):
        """
        Initialize backup service.

        Args:
            database_url: SQLAlchemy Postgres URL for the target database
            schema: Postgres schema to back up/restore (e.g. "fluence_dev")
            backup_dir: Directory to store backups
            max_backups: Maximum number of backups to keep
        """
        self.url = make_url(database_url)
        self.schema = schema
        self.backup_dir = Path(backup_dir)
        self.max_backups = max_backups

        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"BackupService initialized: schema={self.schema} dir={self.backup_dir}")

    def backup_timestamp(self, backup_path: Path) -> datetime:
        """
        Creation time of a backup, parsed from its filename
        (backup_{schema}_%Y%m%d_%H%M%S.dump). st_ctime is unreliable here -
        it's inode metadata-change time, reset by chmod/rsync/restore, so a
        bulk file op can make every backup show the same timestamp.
        """
        try:
            stamp = backup_path.stem.rsplit("_", 2)[-2:]
            return datetime.strptime("_".join(stamp), "%Y%m%d_%H%M%S")
        except (ValueError, IndexError):
            return datetime.fromtimestamp(backup_path.stat().st_ctime)

    def _pg_env(self) -> dict:
        """Env for pg_dump/pg_restore: password via PGPASSWORD, never as a CLI arg."""
        env = os.environ.copy()
        if self.url.password:
            env["PGPASSWORD"] = self.url.password
        return env

    def _connection_args(self) -> list:
        args = ["-h", self.url.host or "localhost", "-p", str(self.url.port or 5432)]
        if self.url.username:
            args += ["-U", self.url.username]
        args += ["-d", self.url.database]
        return args

    def create_backup(self, name: Optional[str] = None) -> Optional[Path]:
        """
        Create a backup of this schema via pg_dump.

        Args:
            name: Exact filename to use instead of the timestamped
                `backup_{schema}_<timestamp>.dump` pattern. Use this for a
                fixed, non-rotating save slot (e.g. an exit save) - a fixed
                name falls outside list_backups()'s glob, so it's never
                touched by cleanup_old_backups() or picked up as "latest".

        Returns:
            Path to the backup file, or None if failed
        """
        try:
            filename = name or f"backup_{self.schema}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.dump"
            backup_path = self.backup_dir / filename

            result = subprocess.run(
                ["pg_dump", *self._connection_args(), "-n", self.schema, "--format=custom", "-f", str(backup_path)],
                env=self._pg_env(),
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                logger.error(f"❌ pg_dump failed: {result.stderr.strip()}")
                return None

            logger.info(f"✅ Backup created: {backup_path.name}")
            if name is None:
                self.cleanup_old_backups()
            return backup_path

        except Exception as e:
            logger.error(f"❌ Backup failed: {e}")
            return None

    def restore_backup(self, backup_path: Optional[Path] = None) -> bool:
        """
        Restore this schema from a backup via pg_restore. Drops and recreates
        existing objects in the schema (--clean) before restoring.

        Args:
            backup_path: Specific backup to restore. If None, uses latest backup.

        Returns:
            True if restore succeeded, False otherwise
        """
        try:
            if backup_path is None:
                backup_path = self.get_latest_backup()

            if backup_path is None:
                logger.warning("No backup found to restore")
                return False

            if not backup_path.exists():
                logger.error(f"Backup file not found: {backup_path}")
                return False

            result = subprocess.run(
                ["pg_restore", *self._connection_args(), "-n", self.schema, "--clean", "--if-exists", str(backup_path)],
                env=self._pg_env(),
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                logger.error(f"❌ pg_restore failed: {result.stderr.strip()}")
                return False

            logger.info(f"✅ Database restored from: {backup_path.name}")
            return True

        except Exception as e:
            logger.error(f"❌ Restore failed: {e}")
            return False

    def get_latest_backup(self) -> Optional[Path]:
        """
        Get the most recent backup file.

        Returns:
            Path to latest backup, or None if no backups exist
        """
        backup_files = self.list_backups()

        if not backup_files:
            return None

        # Return newest backup (already sorted by list_backups)
        return backup_files[0]

    def list_backups(self) -> List[Path]:
        """
        List all backup files for this schema.

        Returns:
            List of backup file paths, sorted by creation time (newest first)
        """
        if not self.backup_dir.exists():
            return []

        backup_files = list(self.backup_dir.glob(f"backup_{self.schema}_*.dump"))
        return sorted(backup_files, key=self.backup_timestamp, reverse=True)

    def cleanup_old_backups(self) -> int:
        """
        Remove old backups exceeding max_backups limit.

        Returns:
            Number of backups deleted
        """
        backup_files = self.list_backups()

        if len(backup_files) <= self.max_backups:
            return 0

        # Delete oldest backups
        files_to_delete = backup_files[self.max_backups:]
        deleted_count = 0

        for backup_file in files_to_delete:
            try:
                backup_file.unlink()
                logger.info(f"🗑️  Deleted old backup: {backup_file.name}")
                deleted_count += 1
            except Exception as e:
                logger.error(f"Failed to delete backup {backup_file.name}: {e}")

        return deleted_count

    def delete_backup(self, backup_path: Path) -> bool:
        """
        Delete a specific backup file.

        Args:
            backup_path: Path to backup file to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            if backup_path.exists() and backup_path.parent == self.backup_dir:
                backup_path.unlink()
                logger.info(f"🗑️  Deleted backup: {backup_path.name}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete backup {backup_path.name}: {e}")
            return False

    def get_backup_size(self, backup_path: Path) -> int:
        """
        Get size of a backup file in bytes.

        Args:
            backup_path: Path to backup file

        Returns:
            Size in bytes, or 0 if file doesn't exist
        """
        try:
            return backup_path.stat().st_size if backup_path.exists() else 0
        except Exception:
            return 0

    def get_stats(self) -> dict:
        """
        Get statistics about backups.

        Returns:
            Dictionary with backup statistics
        """
        backups = self.list_backups()
        total_size = sum(self.get_backup_size(b) for b in backups)

        return {
            'total_backups': len(backups),
            'max_backups': self.max_backups,
            'latest_backup': backups[0].name if backups else None,
            'oldest_backup': backups[-1].name if backups else None,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'backup_dir': str(self.backup_dir),
            'schema': self.schema,
        }

    def verify_backup(self, backup_path: Path) -> bool:
        """
        Verify that a backup file is valid (basic check).

        Args:
            backup_path: Path to backup file

        Returns:
            True if backup appears valid, False otherwise
        """
        try:
            if not backup_path.exists():
                return False

            if backup_path.stat().st_size == 0:
                logger.warning(f"Backup file is empty: {backup_path.name}")
                return False

            # pg_dump custom-format archives start with the "PGDMP" magic bytes.
            with open(backup_path, 'rb') as f:
                header = f.read(5)
                if header != b'PGDMP':
                    logger.warning(f"Backup file is not a valid pg_dump archive: {backup_path.name}")
                    return False

            return True

        except Exception as e:
            logger.error(f"Backup verification failed for {backup_path.name}: {e}")
            return False
