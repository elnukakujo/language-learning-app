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
        self.audio_dir = Path(media_root) / 'audio' if media_root else MediaService().media_root / 'audio'
        self.audio_dir.mkdir(parents=True, exist_ok=True)

        self.model = Qwen3TTSModel.from_pretrained(
            "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
            device_map="cuda:0" if torch.cuda.is_available() else "cpu",
            dtype=torch.bfloat16,
        )
    
    def _get_filename(self) -> Path:
        """
        Get filename for TTS audio file.
        
        Args:
            None
            
        Returns:
            Filename where audio should be saved
        """
        return f"{uuid.uuid4().hex}.wav"
    
    def generate_audio(
        self,
        text: str | list[str]
    ) -> str:
        """
        Generate audio file from text using QwenTTS API.
        
        Args:
            text: Text to convert to speech
            format: Audio format (mp3, wav)
        
        Returns:
            Relative path to generated audio file (e.g., 'audio/tts/word_123.mp3')
        
        Raises:
            ValueError: If text is empty or filename is invalid
            requests.RequestException: If API call fails
            Exception: For other errors
        """
        # Validation
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        try:
            logger.info(f"Generating TTS for: '{text}'")
            
            wavs, sr = self.model.generate_custom_voice(
                text=text,
                speaker="Vivian"
            )

            if isinstance(text, str):
                text = [text]
            
            for idx in range(len(text)):
                filename = self._get_filename()
                output_path = self.audio_dir / filename
                sf.write(output_path, wavs[idx], sr)
                
                logger.info(f"✅ Generated TTS audio: {filename} for text: '{text[idx]}'")
            
            # Return relative path (consistent with MediaService pattern)
            return str(Path('/media/audio') / filename)
            
        except requests.RequestException as e:
            logger.error(f"❌ QwenTTS API error for '{text}': {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Failed to generate audio for '{text}': {e}")
            raise