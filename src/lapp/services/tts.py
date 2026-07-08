import logging
import uuid
from pathlib import Path
import soundfile as sf

from ..utils import detect_text_language, get_qwen_tts_model
from ..utils.detect_language import _LANGUAGES

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

    # ponytail: lazy — TTS model loads on first synth, not when the service is built.
    @property
    def model(self):
        return get_qwen_tts_model()
    
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
            Relative path with forward slashes (e.g., '/media/audio/file.wav' or '/media_dev/audio/file.wav' or '/media_test/audio/file.wav')
        """
        # Get relative path and convert to POSIX format (forward slashes)
        relative = full_path.relative_to(self.media_root)
        # Always return with correct prefix and forward slashes
        return f"/{self.media_root.name}/{relative.as_posix()}"
    
    def generate_audio(
        self,
        text: str,
        language_name: str = None,
    ) -> str | list[str]:
        """
        Generate audio file from text using QwenTTS API.
        
        Args:
            text: Text to convert to speech (string)
        
        Returns:
            Relative path to generated audio file with forward slashes
            (e.g., '/media/audio/abc123.wav')
        
        Raises:
            ValueError: If text is empty
            Exception: For other errors
        """
        # Validation
        if not text:
            raise ValueError("Text cannot be empty")
        
        try:
            logger.info(f"Generating TTS for: {text}")

            if not language_name:
                language_name = detect_text_language(text).name
            logger.info(f"Detected language: {language_name} for text: '{text}'")
            
            wavs, sr = self.model.generate_custom_voice(
                text=[text],
                speaker="Vivian",
                language=language_name if language_name and any(
                    language_name == lang.name for lang in _LANGUAGES.values()
                ) else None,
            )
            
            generated_paths = []
            filename = self._get_filename()
            output_path = self.audio_dir / filename
            sf.write(output_path, wavs[0], sr)
            
            # Get normalized path with forward slashes
            relative_path = self._get_relative_path(output_path)
            generated_paths.append(relative_path)
            
            logger.info(f"✅ Generated TTS audio: {filename} for text: '{text}'")
            
            # Return single path if input was single string, else return list
            return generated_paths[0] if isinstance(text, str) else generated_paths
            
        except Exception as e:
            logger.error(f"❌ Failed to generate audio for '{text}': {e}")
            raise