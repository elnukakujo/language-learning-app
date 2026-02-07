import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List

logger = logging.getLogger(__name__)

class BackupService:
    """
    Service for managing database backups.
    
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
        db_path: Path,
        backup_dir: Path,
        max_backups: int = 10
    ):
        """
        Initialize backup service.
        
        Args:
            db_path: Path to the database file
            backup_dir: Directory to store backups
            max_backups: Maximum number of backups to keep
        """
        self.db_path = Path(db_path)
        self.backup_dir = Path(backup_dir)
        self.max_backups = max_backups
        
        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"BackupService initialized: {self.backup_dir}")
    
    def create_backup(self) -> Optional[Path]:
        """
        Create a backup of the database.
        
        Returns:
            Path to the backup file, or None if failed
        """
        if not self.db_path.exists():
            logger.warning(f"Database file not found: {self.db_path}. Backup skipped.")
            return None
        
        try:
            # Create backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"backup_{timestamp}.sqlite"
            
            # Copy database file
            shutil.copy2(self.db_path, backup_path)
            
            logger.info(f"✅ Backup created: {backup_path.name}")
            
            # Cleanup old backups
            self.cleanup_old_backups()
            
            return backup_path
            
        except Exception as e:
            logger.error(f"❌ Backup failed: {e}")
            return None
    
    def restore_backup(self, backup_path: Optional[Path] = None) -> bool:
        """
        Restore database from a backup.
        
        Args:
            backup_path: Specific backup to restore. If None, uses latest backup.
        
        Returns:
            True if restore succeeded, False otherwise
        """
        try:
            # Get backup file
            if backup_path is None:
                backup_path = self.get_latest_backup()
            
            if backup_path is None:
                logger.warning("No backup found to restore")
                return False
            
            if not backup_path.exists():
                logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # Create emergency backup of current database before restoring
            if self.db_path.exists():
                emergency_backup = self.db_path.parent / f"emergency_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                shutil.copy2(self.db_path, emergency_backup)
                logger.info(f"Emergency backup created: {emergency_backup.name}")
            
            # Restore from backup
            shutil.copy2(backup_path, self.db_path)
            
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
        List all backup files.
        
        Returns:
            List of backup file paths, sorted by creation time (newest first)
        """
        if not self.backup_dir.exists():
            return []
        
        backup_files = list(self.backup_dir.glob("backup_*.sqlite"))
        return sorted(backup_files, key=lambda f: f.stat().st_ctime, reverse=True)
    
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
            'db_path': str(self.db_path),
            'db_exists': self.db_path.exists()
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
            
            # Check if file has content
            if backup_path.stat().st_size == 0:
                logger.warning(f"Backup file is empty: {backup_path.name}")
                return False
            
            # Basic SQLite file check (first 16 bytes should be "SQLite format 3")
            with open(backup_path, 'rb') as f:
                header = f.read(16)
                if not header.startswith(b'SQLite format 3'):
                    logger.warning(f"Backup file is not a valid SQLite database: {backup_path.name}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Backup verification failed for {backup_path.name}: {e}")
            return False