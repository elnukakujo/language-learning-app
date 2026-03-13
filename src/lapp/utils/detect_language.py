from langdetect import detect
import whisper
import os

import logging
logger = logging.getLogger(__name__)

LANGUAGE_CODE_NAME_MAP = {
    'en': 'English',
    'de': 'German',
    'fr': 'French',
    'es': 'Spanish',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh-cn': 'Chinese',
    'zh-tw': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean'
}

audio_detection_model = whisper.load_model("base")

def detect_text_language(text: str) -> str:
    """
    Detects the language of the given text.

    Args:
        text (str): The input text for which to detect the language.

    Returns:
        tuple: The detected language code and name (e.g., ('en', 'English'), ('de', 'German')).
    """
    try:
        language_code = detect(text)
        language_name = LANGUAGE_CODE_NAME_MAP.get(language_code, "Unknown")
        logger.debug(f"Detected language name and code: {language_name}/{language_code} for text: {text}")
        return language_code, language_name
    except Exception as e:
        logger.error(f"Error detecting language: {e}")
        return "unknown", "Unknown"

def detect_audio_language(audio_file_path: str) -> str:
    """
    Detects the language of the given audio file.

    Args:
        audio_file_path (str): The path to the audio file for which to detect the language.

    Returns:
        str: The detected language code (e.g., 'en', 'de').
    """
    try:
        if not os.path.isfile(audio_file_path):
            logger.error(f"Audio file does not exist: {audio_file_path}")
            return "unknown"
        audio = whisper.load_audio(audio_file_path)
        audio = whisper.pad_or_trim(audio)  # Trim/pad to 30s

        mel = whisper.log_mel_spectrogram(
            audio,
            n_mels=audio_detection_model.dims.n_mels
        ).to(audio_detection_model.device)

        _, probs = audio_detection_model.detect_language(mel)

        detected_lang = max(probs, key=probs.get)
        confidence = probs[detected_lang]
        logger.debug(f"Detected audio language: {detected_lang} with confidence: {confidence}")
        return detected_lang
    except Exception as e:
        logger.error(f"Error detecting audio language: {e}")
        return "unknown"