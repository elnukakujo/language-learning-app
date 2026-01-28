# src/lapp/utils/file_handler.py
import uuid
from pathlib import Path
from config import Config

class MediaFileHandler:
    def __init__(self, media_root):
        self.media_root = Path(media_root)
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create media directories if they don't exist"""
        (self.media_root / 'audio').mkdir(parents=True, exist_ok=True)
        (self.media_root / 'images').mkdir(parents=True, exist_ok=True)
    
    def save_image(self, file, subfolder='images'):
        """Save image and return relative path"""
        if not file:
            return None
        
        ext = Path(file.filename).suffix.lower()
        filename = f"{uuid.uuid4().hex}{ext}"
        
        relative_path = Path(subfolder) / filename
        full_path = self.media_root / relative_path
        
        # Ensure subfolder exists
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        file.save(str(full_path))
        return str(relative_path)
    
    def save_audio(self, file):
        """Save audio and return relative path"""
        if not file:
            return None
        
        ext = Path(file.filename).suffix.lower()
        filename = f"{uuid.uuid4().hex}{ext}"
        
        relative_path = Path('audio') / filename
        full_path = self.media_root / relative_path
        
        file.save(str(full_path))
        return str(relative_path)
    
    def delete_file(self, relative_path):
        """Delete a file"""
        if not relative_path:
            return
        
        full_path = self.media_root / relative_path
        if full_path.exists():
            full_path.unlink()
    
    def _is_allowed_image(self, filename):
        """Check if image file type is allowed"""
        ext = Path(filename).suffix.lower().lstrip('.')
        return ext in Config.ALLOWED_IMAGE_EXTENSIONS
    
    def _is_allowed_audio(self, filename):
        """Check if audio file type is allowed"""
        ext = Path(filename).suffix.lower().lstrip('.')
        return ext in Config.ALLOWED_AUDIO_EXTENSIONS