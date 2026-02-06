import logging
import random
import uuid
from pathlib import Path
import requests
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

logger = logging.getLogger(__name__)

class TTSService:
    """
    Service for generating text-to-speech audio using QwenTTS.
    
    This service handles:
    - Audio generation via QwenTTS 3
    - Integration with MediaService/MediaFileHandler
    - File management and storage
    - Error handling and logging
    """
    def __init__(self, media_root: str = None):
        from .media import MediaService
        self.media_root = Path(media_root if media_root else MediaService().media_root)
        self.audio_dir = self.media_root / 'audio'
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.model = Qwen3TTSModel.from_pretrained(
            "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
            device_map="cuda:0" if torch.cuda.is_available() else "cpu",
            dtype=torch.bfloat16,
        )
    
    def _get_filename(self) -> str:
        """
        Get filename for TTS audio file.
        
        Returns:
            Filename where audio should be saved
        """
        return f"{uuid.uuid4().hex}.wav"
    
    def _get_relative_path(self, full_path: Path) -> str:
        """
        Get relative path from media root with forward slashes (cross-platform).
        
        Args:
            full_path: Full file path
            
        Returns:
            Relative path with forward slashes (e.g., '/media/audio/file.wav')
        """
        # Get relative path and convert to POSIX format (forward slashes)
        relative = full_path.relative_to(self.media_root)
        # Always return with /media/ prefix and forward slashes
        return f"/media/{relative.as_posix()}"
    
    def generate_audio(
        self,
        text: str | list[str]
    ) -> str | list[str]:
        """
        Generate audio file from text using QwenTTS API.
        
        Args:
            text: Text to convert to speech (string or list of strings)
        
        Returns:
            Relative path(s) to generated audio file(s) with forward slashes
            (e.g., '/media/audio/abc123.wav' or list of paths)
        
        Raises:
            ValueError: If text is empty
            Exception: For other errors
        """
        # Validation
        if not text:
            raise ValueError("Text cannot be empty")
        
        # Convert single string to list for uniform processing
        text_list = [text] if isinstance(text, str) else text
        
        # Validate all texts
        for t in text_list:
            if not t or not t.strip():
                raise ValueError("Text cannot be empty")
        
        try:
            logger.info(f"Generating TTS for: {text_list}")
            
            wavs, sr = self.model.generate_custom_voice(
                text=text_list,
                speaker="Vivian"
            )
            
            generated_paths = []
            
            for idx, txt in enumerate(text_list):
                filename = self._get_filename()
                output_path = self.audio_dir / filename
                sf.write(output_path, wavs[idx], sr)
                
                # Get normalized path with forward slashes
                relative_path = self._get_relative_path(output_path)
                generated_paths.append(relative_path)
                
                logger.info(f"✅ Generated TTS audio: {filename} for text: '{txt}'")
            
            # Return single path if input was single string, else return list
            return generated_paths[0] if isinstance(text, str) else generated_paths
            
        except Exception as e:
            logger.error(f"❌ Failed to generate audio for '{text}': {e}")
            raise