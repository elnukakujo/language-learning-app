import spacy
import subprocess
import logging

logger = logging.getLogger(__name__)

def load_spacy_model(lang_code: str):
    """Loads the appropriate spaCy model based on the detected language code.
    
    Args:
        lang_code: Language code from langdetect (e.g., 'en', 'fr', 'de')
        
    Returns:
        Loaded spaCy model
    """
    LANG_TO_SPACY_MODEL = {
        "en": "en_core_web_md",
        "fr": "fr_core_news_md",
        "de": "de_core_news_md",
        "es": "es_core_news_md",
        "pt": "pt_core_news_md",
        "it": "it_core_news_md",
        "nl": "nl_core_news_md",
        "el": "el_core_news_md",
        "nb": "nb_core_news_md",
        "lt": "lt_core_news_md",
        "zh-cn": "zh_core_web_md",
        "ja": "ja_core_news_md",
        "ko": "ko_core_news_sm",
        "pl": "pl_core_news_md",
        "ro": "ro_core_news_md",
        "ru": "ru_core_news_md",
        "ca": "ca_core_news_md",
        "da": "da_core_news_md",
        "fi": "fi_core_news_md",
        "hr": "hr_core_news_md",
        "mk": "mk_core_news_md",
        "sl": "sl_core_news_md",
        "sv": "sv_core_news_md",
        "uk": "uk_core_news_md",
    }

    model_name = LANG_TO_SPACY_MODEL.get(lang_code)
    if not model_name:
        raise ValueError(f"No spaCy model found for language code '{lang_code}'")
    
    return spacy.load(model_name)