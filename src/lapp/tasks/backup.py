import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask

logger = logging.getLogger(__name__)

def register_backup_tasks(scheduler: BackgroundScheduler, app: Flask):
    """
    Backup after every BACKUP_AFTER_ACTIONS DB mutations. Polls every 60s;
    actual backup runs in the poll tick, not in any request thread.
    """
    threshold = app.config.get('BACKUP_AFTER_ACTIONS', 100)

    scheduler.add_job(
        func=check_and_backup,
        trigger=IntervalTrigger(seconds=60),
        id='automatic_backup',
        name=f'Automatic database backup (after {threshold} mutations)',
        replace_existing=True,
        args=[app]
    )
    logger.info(f"✅ Scheduled job: automatic_backup (every {threshold} mutations, polled every 60s)")

def check_and_backup(app: Flask):
    """Poll the mutation counter; create a backup once it crosses the threshold."""
    from lapp.core.database import db_manager
    try:
        count = db_manager.get_mutation_count()
    except Exception as e:
        logger.error(f"❌ Could not read mutation counter: {e}")
        return
    if count >= app.config.get('BACKUP_AFTER_ACTIONS', 100):
        logger.info(f"⏰ Mutation counter at {count}, creating automatic backup")
        create_automatic_backup(app)

def create_automatic_backup(app: Flask) -> bool:
    """Create a backup via app.backup_manager (no duplicate BackupService)."""
    with app.app_context():
        try:
            backup_path = app.backup_manager.create_backup()
            if backup_path:
                stats = app.backup_manager.get_stats()
                logger.info(
                    f"✅ Automatic backup: {backup_path.name} "
                    f"(Total: {stats['total_backups']}/{stats['max_backups']})"
                )
                return True
            logger.warning("⚠️ Automatic backup was not created")
            return False
        except Exception as e:
            logger.error(f"❌ Automatic backup error: {e}", exc_info=True)
            return False
