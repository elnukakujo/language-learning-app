"""
Database backup management endpoints.

Provides API endpoints for:
- Creating manual backups
- Restoring from backups
- Listing available backups
- Getting backup statistics
- Deleting old backups
"""
import logging
from flask import Blueprint, jsonify, request, current_app
from datetime import datetime

logger = logging.getLogger(__name__)

bp = Blueprint('backup', __name__, url_prefix='/api/backup')

@bp.route('/create', methods=['POST'])
def create_backup():
    """
    Create a manual database backup.
    
    Returns:
        JSON response with backup information
    
    Example:
        POST /api/backup/create
        
        Response:
        {
            "success": true,
            "backup_file": "backup_20250128_143022.sqlite",
            "path": "/path/to/backups/backup_20250128_143022.sqlite",
            "size_mb": 2.45
        }
    """
    try:
        backup_mgr = current_app.backup_manager
        backup_path = backup_mgr.backup()
        
        if backup_path:
            # Get file size
            size_mb = round(backup_path.stat().st_size / (1024 * 1024), 2)
            
            return jsonify({
                'success': True,
                'backup_file': backup_path.name,
                'path': str(backup_path),
                'size_mb': size_mb,
                'created_at': datetime.now().isoformat()
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Backup creation failed'
            }), 500
            
    except Exception as e:
        logger.error(f"Backup creation error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/restore', methods=['POST'])
def restore_backup():
    """
    Restore database from a backup.
    
    Request body (optional):
        {
            "backup_file": "backup_20250128_143022.sqlite"
        }
    
    If no backup_file specified, restores from latest backup.
    
    Returns:
        JSON response with restore status
    
    Example:
        POST /api/backup/restore
        {
            "backup_file": "backup_20250128_143022.sqlite"
        }
        
        Response:
        {
            "success": true,
            "restored_from": "backup_20250128_143022.sqlite",
            "message": "Database restored successfully"
        }
    """
    try:
        backup_mgr = current_app.backup_manager
        
        # Get optional backup file from request
        data = request.get_json() or {}
        backup_file = data.get('backup_file')
        
        # Construct full path if backup_file specified
        backup_path = None
        if backup_file:
            backup_path = backup_mgr.backup_dir / backup_file
            
            if not backup_path.exists():
                return jsonify({
                    'success': False,
                    'error': f'Backup file not found: {backup_file}'
                }), 404
        
        # Restore from specified backup or latest
        success = backup_mgr.restore(backup_path)
        
        if success:
            restored_from = backup_path.name if backup_path else backup_mgr.get_latest_backup().name
            
            return jsonify({
                'success': True,
                'restored_from': restored_from,
                'message': 'Database restored successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Restore failed'
            }), 500
            
    except Exception as e:
        logger.error(f"Restore error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/list', methods=['GET'])
def list_backups():
    """
    List all available backups with details.
    
    Returns:
        JSON response with list of backups
    
    Example:
        GET /api/backup/list
        
        Response:
        {
            "total": 15,
            "backups": [
                {
                    "filename": "backup_20250128_143022.sqlite",
                    "size_mb": 2.45,
                    "created_at": "2025-01-28T14:30:22",
                    "age_days": 0
                },
                ...
            ]
        }
    """
    try:
        backup_mgr = current_app.backup_manager
        backups = backup_mgr.list_backups()
        
        backup_list = []
        for backup_path in backups:
            stat = backup_path.stat()
            created_timestamp = stat.st_ctime
            created_dt = datetime.fromtimestamp(created_timestamp)
            age_days = (datetime.now() - created_dt).days
            
            backup_list.append({
                'filename': backup_path.name,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'size_bytes': stat.st_size,
                'created_at': created_dt.isoformat(),
                'age_days': age_days,
                'is_latest': backup_path == backup_mgr.get_latest_backup()
            })
        
        return jsonify({
            'total': len(backup_list),
            'backups': backup_list
        })
        
    except Exception as e:
        logger.error(f"List backups error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/info', methods=['GET'])
def backup_info():
    """
    Get backup system information and statistics.
    
    Returns:
        JSON response with backup statistics
    
    Example:
        GET /api/backup/info
        
        Response:
        {
            "total_backups": 15,
            "max_backups": 30,
            "latest_backup": "backup_20250128_143022.sqlite",
            "latest_backup_age_hours": 2,
            "backup_dir": "/path/to/backups",
            "scheduler_running": true,
            "backup_interval_hours": 24,
            "total_size_mb": 36.75
        }
    """
    try:
        backup_mgr = current_app.backup_manager
        info = backup_mgr.get_backup_info()
        
        # Add additional calculated fields
        backups = backup_mgr.list_backups()
        
        # Calculate total size
        total_size = sum(b.stat().st_size for b in backups)
        info['total_size_mb'] = round(total_size / (1024 * 1024), 2)
        
        # Add latest backup age
        latest = backup_mgr.get_latest_backup()
        if latest:
            created_timestamp = latest.stat().st_ctime
            created_dt = datetime.fromtimestamp(created_timestamp)
            age_hours = (datetime.now() - created_dt).total_seconds() / 3600
            info['latest_backup_age_hours'] = round(age_hours, 1)
        else:
            info['latest_backup_age_hours'] = None
        
        return jsonify(info)
        
    except Exception as e:
        logger.error(f"Backup info error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/delete/<backup_file>', methods=['DELETE'])
def delete_backup(backup_file: str):
    """
    Delete a specific backup file.
    
    Args:
        backup_file: Name of the backup file to delete
    
    Returns:
        JSON response with deletion status
    
    Example:
        DELETE /api/backup/delete/backup_20250128_143022.sqlite
        
        Response:
        {
            "success": true,
            "message": "Backup deleted successfully",
            "deleted_file": "backup_20250128_143022.sqlite"
        }
    """
    try:
        backup_mgr = current_app.backup_manager
        backup_path = backup_mgr.backup_dir / backup_file
        
        # Security check: ensure it's a backup file
        if not backup_file.startswith('backup_') or not backup_file.endswith('.sqlite'):
            return jsonify({
                'success': False,
                'error': 'Invalid backup filename'
            }), 400
        
        if not backup_path.exists():
            return jsonify({
                'success': False,
                'error': f'Backup file not found: {backup_file}'
            }), 404
        
        # Don't allow deleting the latest backup if it's the only one
        backups = backup_mgr.list_backups()
        if len(backups) == 1:
            return jsonify({
                'success': False,
                'error': 'Cannot delete the only backup'
            }), 400
        
        # Delete the file
        backup_path.unlink()
        logger.info(f"Deleted backup: {backup_file}")
        
        return jsonify({
            'success': True,
            'message': 'Backup deleted successfully',
            'deleted_file': backup_file
        })
        
    except Exception as e:
        logger.error(f"Delete backup error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/cleanup', methods=['POST'])
def cleanup_old_backups():
    """
    Manually trigger cleanup of old backups.
    
    Removes backups exceeding the configured max_backups limit.
    
    Returns:
        JSON response with cleanup statistics
    
    Example:
        POST /api/backup/cleanup
        
        Response:
        {
            "success": true,
            "deleted_count": 5,
            "remaining_count": 30,
            "message": "Cleanup completed"
        }
    """
    try:
        backup_mgr = current_app.backup_manager
        
        # Get count before cleanup
        before_count = len(backup_mgr.list_backups())
        
        # Trigger cleanup
        backup_mgr._cleanup_old_backups()
        
        # Get count after cleanup
        after_count = len(backup_mgr.list_backups())
        deleted_count = before_count - after_count
        
        return jsonify({
            'success': True,
            'deleted_count': deleted_count,
            'remaining_count': after_count,
            'message': 'Cleanup completed'
        })
        
    except Exception as e:
        logger.error(f"Cleanup error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500