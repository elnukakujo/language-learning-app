import spacy
import logging

logger = logging.getLogger(__name__)

def load_spacy_model(spacy_model_id: str):
    """Loads the appropriate spaCy model based on the detected language code.
    
    Args:
        lang_code: Language code from langdetect (e.g., 'en', 'fr', 'de')
        
    Returns:
        Loaded spaCy model
    """
    
    if not spacy_model_id:
        raise ValueError(f"No spaCy model found for language code '{spacy_model_id}'")
    
    return spacy.load(spacy_model_id)