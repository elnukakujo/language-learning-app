import logging
import uuid
from pathlib import Path

from ..utils import synthesize_speech, detect_text_language

logger = logging.getLogger(__name__)

# Verified against http://192.168.1.139:8880/voices (Kokoro server)
# Convention: {lang}_{gender} — en_f, en_m, es_f, es_m, etc.
_VOICE_MAP: dict[str, dict[str, str]] = {
    "en": {"female": "en_f", "male": "en_m"},
    "es": {"female": "es_f", "male": "es_m"},
    "fr": {"female": "fr_f"},                          # no male voice
    "ja": {"female": "ja_f", "male": "ja_m"},
    "zh": {"female": "zh_f", "male": "zh_m"},
    "hi": {"female": "hi_f"},                          # no male voice
    "it": {"female": "it_f"},                          # no male voice
    "pt": {"female": "pt_f"},                          # no male voice
}
_VOICE_FALLBACK = "en_f"

class TTSService:
    """
    Service for generating text-to-speech audio via a configurable TTS API endpoint.

    This service handles:
    - Audio generation via LAPP_TTS_API_BASE_URL
    - Integration with MediaService/MediaFileHandler
    - File management and storage
    - Error handling and logging
    """
    def __init__(self, media_root: str = None):
        from .media import MediaService
        self.media_root = Path(media_root if media_root else MediaService().media_root)
        self.audio_dir = self.media_root / 'audio'
        self.audio_dir.mkdir(parents=True, exist_ok=True)

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
        api: dict | None = None,
    ) -> str | list[str]:
        """
        Generate audio file from text using the configured TTS API endpoint.
        
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

        if not api or not api.get("base_url"):
            raise ValueError("No TTS API configured for this user")

        try:
            logger.info(f"Generating TTS for: {text}")

            # Voice resolution: explicit override > language+gender > language-female > fallback
            if not api.get("voice"):
                try:
                    lang = detect_text_language(text)
                    iso1 = lang.iso1 if lang else "unknown"
                    gender = api.get("voice_gender") or "female"
                    voices = _VOICE_MAP.get(iso1, {})
                    # ponytail: if male voice doesn't exist for this language, fall back to female
                    voice = voices.get(gender) or voices.get("female") or _VOICE_FALLBACK
                    api = {**api, "voice": voice}
                    logger.info(f"Auto-detected voice '{voice}' (lang={iso1}, gender={gender})")
                except Exception:
                    api = {**api, "voice": _VOICE_FALLBACK}
                    logger.info(f"Voice detection failed, using fallback '{_VOICE_FALLBACK}'")

            wav_bytes = synthesize_speech(**api, text=text)

            generated_paths = []
            filename = self._get_filename()
            output_path = self.audio_dir / filename
            output_path.write_bytes(wav_bytes)

            # Get normalized path with forward slashes
            relative_path = self._get_relative_path(output_path)
            generated_paths.append(relative_path)
            
            logger.info(f"✅ Generated TTS audio: {filename} for text: '{text}'")
            
            # Return single path if input was single string, else return list
            return generated_paths[0] if isinstance(text, str) else generated_paths
            
        except Exception as e:
            logger.error(f"❌ Failed to generate audio for '{text}': {e}")
            raise