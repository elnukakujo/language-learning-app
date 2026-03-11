from langdetect import detect

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

def get_language_name(text: str) -> str:
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