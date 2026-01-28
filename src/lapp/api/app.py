import logging
import os
from flask import Flask, jsonify
from flask_cors import CORS

from ..core.database import init_db
from ..core.backup import init_backup_manager
from config import config, INSTANCE_DIR, BACKUP_DIR

logger = logging.getLogger(__name__)


def create_app(config_name: str = 'default') -> Flask:
    """
    Application factory pattern for Flask.
    
    Args:
        config_name: Configuration to use ('development', 'testing', 'production')
    
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Configure logging
    configure_logging(app)
    
    # Enable CORS for frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize extensions
    initialize_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register CLI commands
    register_commands(app)

    # Register health check endpoint
    register_health_check(app)
    
    logger.info(f"🚀 Flask app created with config: {config_name}")
    
    return app


def configure_logging(app: Flask) -> None:
    """Configure application logging."""
    log_level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def initialize_extensions(app: Flask) -> None:
    """Initialize Flask extensions and database."""

    # Detect the real process (not the reloader)
    is_main_process = (
        not app.debug
        or os.environ.get("WERKZEUG_RUN_MAIN") == "true"
    )

    # Initialize database (safe to do twice, usually)
    db = init_db(app)
    logger.info("✅ Database initialized")

    # Initialize backup manager
    db_path = INSTANCE_DIR / 'languages.db'
    backup_mgr = init_backup_manager(
        db_path=db_path,
        backup_dir=BACKUP_DIR,
        config=app.config
    )

    # Start automatic backups ONLY once
    if is_main_process and not app.config.get('TESTING'):
        backup_mgr.start_scheduler()
        logger.info("✅ Backup scheduler started")

    app.backup_manager = backup_mgr


def register_blueprints(app: Flask) -> None:
    """Register all API blueprints."""
    
    from ..api.routes import (
        language_bp,
        unit_bp
    )
    
    # Register blueprints
    blueprints = [
        language_bp,
        unit_bp
    ]
    
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        logger.info(f"✅ Registered blueprint: {blueprint.name}")


def register_error_handlers(app: Flask) -> None:
    """Register error handlers for common HTTP errors."""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': str(error)
        }), 400
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"Unhandled exception: {error}", exc_info=True)
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500


def register_commands(app: Flask) -> None:
    """Register custom CLI commands."""
    
    @app.cli.command()
    def init_db():
        """Initialize the database."""
        from ..core.database import db_manager
        db_manager.create_tables()
        print("✅ Database initialized")
    
    @app.cli.command()
    def backup_now():
        """Create a manual backup."""
        backup_path = app.backup_manager.backup()
        if backup_path:
            print(f"✅ Backup created: {backup_path}")
        else:
            print("❌ Backup failed")
    
    @app.cli.command()
    def restore_backup():
        """Restore from latest backup."""
        success = app.backup_manager.restore()
        if success:
            print("✅ Database restored")
        else:
            print("❌ Restore failed")


# Health check endpoint
def register_health_check(app: Flask) -> None:
    """Register health check endpoint."""
    
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'environment': app.config.get('ENV', 'unknown')
        })