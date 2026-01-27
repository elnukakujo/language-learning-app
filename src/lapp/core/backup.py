import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

class BackupManager:
    """
    Manages database backups with automatic scheduling and cleanup.
    
    Features:
    - Automatic scheduled backups
    - Manual backup/restore
    - Automatic cleanup of old backups
    - Configurable retention policies
    """
    
    def __init__(
        self,
        db_path: Path,
        backup_dir: Path,
        max_backups: int = 30,
        backup_interval_minutes: int = 60
    ):
        """
        Initialize the backup manager.
        
        Args:
            db_path: Path to the database file
            backup_dir: Directory to store backups
            max_backups: Maximum number of backups to keep
            backup_interval_minutes: Minutes between automatic backups
        """
        self.db_path = Path(db_path)
        self.backup_dir = Path(backup_dir)
        self.max_backups = max_backups
        self.backup_interval_minutes = backup_interval_minutes
        self.scheduler: Optional[BackgroundScheduler] = None
        
        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"BackupManager initialized: {self.backup_dir}")
    
    def backup(self) -> Optional[Path]:
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
            
            logger.info(f"✅ Backup created: {backup_path}")
            
            # Cleanup old backups
            self._cleanup_old_backups()
            
            return backup_path
            
        except Exception as e:
            logger.error(f"❌ Backup failed: {e}")
            return None
    
    def restore(self, backup_path: Optional[Path] = None) -> bool:
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
            
            # Create a backup of current database before restoring
            if self.db_path.exists():
                emergency_backup = self.db_path.parent / f"emergency_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                shutil.copy2(self.db_path, emergency_backup)
                logger.info(f"Emergency backup created: {emergency_backup}")
            
            # Restore from backup
            shutil.copy2(backup_path, self.db_path)
            
            logger.info(f"✅ Database restored from: {backup_path}")
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
        
        # Return newest backup
        return max(backup_files, key=lambda f: f.stat().st_ctime)
    
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
    
    def _cleanup_old_backups(self) -> None:
        """Remove old backups exceeding max_backups limit."""
        backup_files = self.list_backups()
        
        if len(backup_files) <= self.max_backups:
            return
        
        # Delete oldest backups
        files_to_delete = backup_files[self.max_backups:]
        
        for backup_file in files_to_delete:
            try:
                backup_file.unlink()
                logger.info(f"🗑️  Deleted old backup: {backup_file.name}")
            except Exception as e:
                logger.error(f"Failed to delete backup {backup_file}: {e}")
    
    def start_scheduler(self) -> None:
        """Start automatic backup scheduler."""
        if self.scheduler is not None:
            logger.warning("Backup scheduler already running")
            return
        
        self.scheduler = BackgroundScheduler()
        
        # Schedule backup job
        self.scheduler.add_job(
            func=self.backup,
            trigger=IntervalTrigger(minutes=self.backup_interval_minutes),
            id='database_backup',
            name='Database Backup',
            replace_existing=True
        )
        
        self.scheduler.start()
        
        logger.info(f"🔄 Backup scheduler started (interval: {self.backup_interval_minutes} minutes)")
    
    def stop_scheduler(self) -> None:
        """Stop automatic backup scheduler."""
        if self.scheduler is None:
            return
        
        self.scheduler.shutdown()
        self.scheduler = None
        
        logger.info("⏹️  Backup scheduler stopped")
    
    def get_backup_info(self) -> dict:
        """
        Get information about current backup status.
        
        Returns:
            Dictionary with backup statistics
        """
        backups = self.list_backups()
        
        return {
            'total_backups': len(backups),
            'max_backups': self.max_backups,
            'latest_backup': self.get_latest_backup().name if backups else None,
            'backup_dir': str(self.backup_dir),
            'scheduler_running': self.scheduler is not None,
            'backup_interval_minutes': self.backup_interval_minutes
        }


# Global instance (initialized in app.py)
backup_manager: Optional[BackupManager] = None


def init_backup_manager(db_path: Path, backup_dir: Path, config: dict) -> BackupManager:
    """
    Initialize global backup manager.
    
    Args:
        db_path: Path to database file
        backup_dir: Path to backup directory
        config: Configuration dictionary with backup settings
    
    Returns:
        Initialized BackupManager instance
    """
    global backup_manager
    
    backup_manager = BackupManager(
        db_path=db_path,
        backup_dir=backup_dir,
        max_backups=config.get('MAX_BACKUPS', 30),
        backup_interval_minutes=config.get('BACKUP_INTERVAL_MINUTES', 60)
    )
    
    return backup_manager