import logging
logger = logging.getLogger(__name__)

from .detect_language import _LANGUAGES
from .spacy_model import load_spacy_model

# ── POS tag → canonical word-type string ────────────────────────────────────
_SPACY_POS_TO_TYPE: dict[str, str] = {
    "NOUN":    "noun",
    "PROPN":   "noun",        # proper noun → treat as noun
    "VERB":    "verb",
    "AUX":     "auxiliary",
    "ADJ":     "adjective",
    "ADV":     "adverb",
    "PRON":    "pronoun",
    "DET":     "article",     # determiners include articles
    "ADP":     "preposition",
    "CCONJ":   "conjunction",
    "SCONJ":   "conjunction",
    "PART":    "particle",
    "INTJ":    "interjection",
    "NUM":     "numeral",
    "X":       "",
    "PUNCT":   "",
    "SPACE":   "",
    "SYM":     "",
}

def get_word_type(word_text: str, iso1: str) -> str:
    """
    Return the coarse word type (POS) for *word_text* in language *iso1*.

    Uses the spaCy model registered in ``_LANGUAGES`` for that ISO 639-1 code.
    Falls back to ``""`` when the language is not in ``_LANGUAGES`` or spaCy
    assigns an unknown / punctuation tag.

    Args:
        word_text: Surface form, e.g. ``"courir"`` or ``"北京"``.
        iso1:      ISO 639-1 code, e.g. ``"fr"`` or ``"zh"``.

    Returns:
        One of the canonical type strings defined in the project, or ``""``.

    Examples:
        get_word_type("courir",   "fr")  # → "verb"
        get_word_type("北京",     "zh")  # → "noun"
        get_word_type("laufen",   "de")  # → "verb"
        get_word_type("beautiful","en")  # → "adjective"
    """
    lang = iso1.split("-")[0].lower()
    language = _LANGUAGES.get(lang)
    if language is None:
        logger.debug("get_word_type: no spaCy model for iso1=%r", iso1)
        return ""

    try:
        nlp = load_spacy_model(language.spacy_model)
        doc = nlp(word_text)
        if not doc:
            return ""

        # For single-word lookups the first non-space token is authoritative.
        for token in doc:
            if token.pos_ not in ("SPACE", "PUNCT", ""):
                word_type = _SPACY_POS_TO_TYPE.get(token.pos_, "")

                # spaCy tags Chinese classifiers explicitly
                if token.pos_ == "NOUN" and token.tag_ == "NNB":
                    word_type = "classifier"

                # Modal auxiliaries (English "can", "must", German "können" …)
                if token.pos_ == "AUX" and token.morph.get("VerbType") == ["Mod"]:
                    word_type = "modal"

                return word_type
        return ""

    except Exception:
        logger.exception("get_word_type(%r, %r) failed", word_text, iso1)
        return ""