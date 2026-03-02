from langdetect import detect

import logging
logger = logging.getLogger(__name__)

def get_language_name(text: str) -> str:
    """
    Detects the language of the given text.

    Args:
        text (str): The input text for which to detect the language.

    Returns:
        str: The detected language code (e.g., 'en' for English, 'de' for German).
    """
    try:
        language = detect(text)
        logger.debug(f"Detected language: {language} for text: {text}")
        return language
    except Exception as e:
        logger.error(f"Error detecting language: {e}")
        return "unknown"