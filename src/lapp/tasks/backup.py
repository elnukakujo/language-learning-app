import logging
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask

logger = logging.getLogger(__name__)

def register_backup_tasks(scheduler: BackgroundScheduler, app: Flask):
    """
    Register backup-related scheduled tasks.
    Uses interval-based scheduling since app doesn't run 24/7.
    
    Args:
        scheduler: APScheduler instance
        app: Flask app instance for accessing config
    """
    # Get backup interval from config (default: 60 minutes)
    backup_interval = app.config.get('BACKUP_INTERVAL_MINUTES', 60)
    
    # Interval-based backup (runs every X minutes while app is running)
    scheduler.add_job(
        func=create_automatic_backup,
        trigger=IntervalTrigger(minutes=backup_interval),
        id='automatic_backup',
        name=f'Automatic database backup (every {backup_interval} minutes)',
        replace_existing=True,
        args=[app]
    )
    logger.info(f"✅ Scheduled job: automatic_backup (every {backup_interval} minutes)")

def create_automatic_backup(app: Flask):
    """
    Scheduled task: Create automatic database backup.
    
    This function is called by APScheduler and must handle app context properly.
    """
    with app.app_context():
        try:
            from lapp.services.backup import BackupService

            # Get config values from app (inside app context)
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            db_path = Path(db_uri.replace('sqlite:///', ''))
            backup_dir = Path(app.config['BACKUP_ROOT'])
            max_backups = app.config['MAX_BACKUPS']

            # Create backup service (no app context dependency)
            backup_service = BackupService(
                db_path=db_path,
                backup_dir=backup_dir,
                max_backups=max_backups
            )

            # Create backup
            backup_path = backup_service.create_backup()

            if backup_path:
                stats = backup_service.get_stats()
                logger.info(
                    f"✅ Automatic backup: {backup_path.name} "
                    f"(Total: {stats['total_backups']}/{stats['max_backups']})"
                )
            else:
                logger.warning("⚠️ Automatic backup was not created")
        
        except Exception as e:
            logger.error(f"❌ Automatic backup error: {e}", exc_info=True)