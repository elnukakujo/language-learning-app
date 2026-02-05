import logging
import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

logger = logging.getLogger(__name__)


class AppScheduler:
    """
    Centralized scheduler for all background tasks.
    Manages APScheduler instance and task registration.
    Uses interval-based scheduling for apps that don't run 24/7.
    """
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self._running = False
    
    def init_app(self, app: Flask):
        """
        Initialize scheduler with Flask app.
        
        Args:
            app: Flask application instance
        """
        self.app = app
        
        # Register all scheduled tasks
        self._register_tasks()
        
        logger.info("✅ AppScheduler initialized with Flask app")
    
    def _register_tasks(self):
        """Register all scheduled tasks from different modules."""
        # Import task registration functions
        from ..tasks.backup import register_backup_tasks
        from ..tasks.tts import register_tts_tasks
        
        # Register tasks from each module
        register_backup_tasks(self.scheduler, self.app)
        register_tts_tasks(self.scheduler, self.app)
        
        logger.info("✅ All scheduled tasks registered")
    
    def start(self):
        """Start the scheduler."""
        if not self._running:
            self.scheduler.start()
            self._running = True
            logger.info("✅ AppScheduler started")
    
    def shutdown(self):
        """Shutdown the scheduler gracefully."""
        if self._running:
            self.scheduler.shutdown()
            self._running = False
            logger.info("🛑 AppScheduler stopped")
    
    def is_running(self) -> bool:
        """Check if scheduler is running."""
        return self._running
    
    def get_jobs(self):
        """Get all scheduled jobs."""
        return self.scheduler.get_jobs()


# Global scheduler instance
app_scheduler = AppScheduler()


def init_scheduler(app: Flask) -> AppScheduler:
    """
    Initialize scheduler with Flask app.
    
    Args:
        app: Flask application instance
    
    Returns:
        AppScheduler instance
    """
    # Detect the real process (not the reloader)
    is_main_process = (
        not app.debug
        or os.environ.get("WERKZEUG_RUN_MAIN") == "true"
    )
    
    if is_main_process and not app.config.get('TESTING'):
        app_scheduler.init_app(app)
        app_scheduler.start()
        
        # Register cleanup on shutdown
        import atexit
        atexit.register(app_scheduler.shutdown)
        
        logger.info("✅ Scheduler initialized and started")
    else:
        logger.info("⏭️ Skipping scheduler initialization (reloader or testing)")
    
    return app_scheduler