import logging
from flask import Blueprint, request, jsonify, send_from_directory, current_app, abort
from pathlib import Path

from ...utils import MediaFileHandler

logger = logging.getLogger(__name__)

bp = Blueprint('media', __name__, url_prefix='/media')

# Initialize file handler
file_handler = None


def get_file_handler() -> MediaFileHandler:
    """Get or create MediaFileHandler instance."""
    global file_handler
    if file_handler is None:
        media_root = current_app.config['MEDIA_ROOT']
        file_handler = MediaFileHandler(media_root)
    return file_handler


@bp.route('/<path:filename>')
def serve_media(filename: str):
    """
    Serve media files (images, audio).
    
    Args:
        filename: Relative path to media file (e.g., 'images/cat.jpeg')
    
    Returns:
        Media file or 404 if not found
    
    Example:
        GET /media/images/cat.jpeg
        GET /media/audio/hello_en_abc123.mp3
    """
    try:
        media_root = Path(current_app.config['MEDIA_ROOT'])
        file_path = media_root / filename
        
        # Security: Prevent directory traversal attacks
        try:
            file_path = file_path.resolve()
            file_path.relative_to(media_root.resolve())
        except ValueError:
            logger.warning(f"Directory traversal attempt: {filename}")
            abort(403)  # Forbidden
        
        # Check if file exists
        if not file_path.exists():
            logger.warning(f"Media file not found: {filename}")
            abort(404)
        
        # Serve the file
        return send_from_directory(
            media_root,
            filename,
            as_attachment=False
        )
        
    except Exception as e:
        logger.error(f"Error serving media: {e}", exc_info=True)
        abort(500)


@bp.route('/upload/image', methods=['POST'])
def upload_image():
    """
    Upload an image file.
    
    Request:
        multipart/form-data with 'file' field
        Optional 'category' field (default: 'images')
    
    Returns:
        JSON response with file path
    
    Example:
        POST /media/upload/image
        Content-Type: multipart/form-data
        
        file: [binary image data]
        category: vocabulary
        
        Response:
        {
            "success": true,
            "file_path": "images/vocabulary/abc123def456.jpg",
            "url": "/media/images/vocabulary/abc123def456.jpg"
        }
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        # Check if file was actually selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Get optional category
        category = request.form.get('category', 'images')
        
        # Validate file type
        handler = get_file_handler()
        if not handler._is_allowed_image(file.filename):
            return jsonify({
                'success': False,
                'error': f'File type not allowed. Allowed types: {current_app.config["ALLOWED_IMAGE_EXTENSIONS"]}'
            }), 400
        
        # Check file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        max_size = current_app.config.get('MAX_IMAGE_SIZE', 5 * 1024 * 1024)
        if file_size > max_size:
            return jsonify({
                'success': False,
                'error': f'File too large. Maximum size: {max_size / (1024*1024)}MB'
            }), 400
        
        # Save the file
        relative_path = handler.save_image(file, subfolder=category)
        
        if relative_path:
            logger.info(f"Uploaded image: {relative_path}")
            
            return jsonify({
                'success': True,
                'file_path': relative_path,
                'url': f'/media/{relative_path}',
                'size_bytes': file_size
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to save file'
            }), 500
            
    except Exception as e:
        logger.error(f"Image upload error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/upload/audio', methods=['POST'])
def upload_audio():
    """
    Upload an audio file.
    
    Request:
        multipart/form-data with 'file' field
    
    Returns:
        JSON response with file path
    
    Example:
        POST /media/upload/audio
        Content-Type: multipart/form-data
        
        file: [binary audio data]
        
        Response:
        {
            "success": true,
            "file_path": "audio/abc123def456.mp3",
            "url": "/media/audio/abc123def456.mp3"
        }
    """
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Validate file type
        handler = get_file_handler()
        if not handler._is_allowed_audio(file.filename):
            return jsonify({
                'success': False,
                'error': f'File type not allowed. Allowed types: {current_app.config["ALLOWED_AUDIO_EXTENSIONS"]}'
            }), 400
        
        # Check file size
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        
        max_size = current_app.config.get('MAX_AUDIO_SIZE', 10 * 1024 * 1024)
        if file_size > max_size:
            return jsonify({
                'success': False,
                'error': f'File too large. Maximum size: {max_size / (1024*1024)}MB'
            }), 400
        
        # Save the file
        relative_path = handler.save_audio(file)
        
        if relative_path:
            logger.info(f"Uploaded audio: {relative_path}")
            
            return jsonify({
                'success': True,
                'file_path': relative_path,
                'url': f'/media/{relative_path}',
                'size_bytes': file_size
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to save file'
            }), 500
            
    except Exception as e:
        logger.error(f"Audio upload error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/delete', methods=['DELETE'])
def delete_media():
    """
    Delete a media file.
    
    Request body:
        {
            "file_path": "images/cat.jpeg"
        }
    
    Returns:
        JSON response with deletion status
    
    Example:
        DELETE /media/delete
        {
            "file_path": "images/cat.jpeg"
        }
        
        Response:
        {
            "success": true,
            "message": "File deleted successfully",
            "deleted_file": "images/cat.jpeg"
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'file_path' not in data:
            return jsonify({
                'success': False,
                'error': 'file_path is required'
            }), 400
        
        file_path = data['file_path']
        
        # Security: validate path
        media_root = Path(current_app.config['MEDIA_ROOT'])
        full_path = media_root / file_path
        
        try:
            full_path = full_path.resolve()
            full_path.relative_to(media_root.resolve())
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid file path'
            }), 400
        
        # Check if file exists
        if not full_path.exists():
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        # Delete the file
        handler = get_file_handler()
        handler.delete_file(file_path)
        
        logger.info(f"Deleted media file: {file_path}")
        
        return jsonify({
            'success': True,
            'message': 'File deleted successfully',
            'deleted_file': file_path
        })
        
    except Exception as e:
        logger.error(f"Delete media error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/info/<path:filename>', methods=['GET'])
def media_info(filename: str):
    """
    Get information about a media file.
    
    Args:
        filename: Relative path to media file
    
    Returns:
        JSON response with file information
    
    Example:
        GET /media/info/images/cat.jpeg
        
        Response:
        {
            "filename": "cat.jpeg",
            "path": "images/cat.jpeg",
            "size_mb": 0.45,
            "size_bytes": 471859,
            "type": "image",
            "extension": ".jpeg",
            "exists": true
        }
    """
    try:
        media_root = Path(current_app.config['MEDIA_ROOT'])
        file_path = media_root / filename
        
        # Security check
        try:
            file_path = file_path.resolve()
            file_path.relative_to(media_root.resolve())
        except ValueError:
            abort(403)
        
        if not file_path.exists():
            return jsonify({
                'filename': file_path.name,
                'path': filename,
                'exists': False
            }), 404
        
        # Get file info
        stat = file_path.stat()
        extension = file_path.suffix.lower()
        
        # Determine type
        handler = get_file_handler()
        if handler._is_allowed_image(file_path.name):
            file_type = 'image'
        elif handler._is_allowed_audio(file_path.name):
            file_type = 'audio'
        else:
            file_type = 'unknown'
        
        return jsonify({
            'filename': file_path.name,
            'path': filename,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'size_bytes': stat.st_size,
            'type': file_type,
            'extension': extension,
            'exists': True,
            'url': f'/media/{filename}'
        })
        
    except Exception as e:
        logger.error(f"Media info error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500