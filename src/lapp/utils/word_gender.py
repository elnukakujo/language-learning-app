import logging
logger = logging.getLogger(__name__)

from .detect_language import _LANGUAGES
from .spacy_model import load_spacy_model

# spaCy morphology gender values → normalised strings
_SPACY_GENDER_TO_STR: dict[str, str] = {
    "Masc": "m",
    "Fem":  "f",
    "Neut": "n",
    "Com":  "c",   # Danish / Swedish common gender
}

# Languages whose grammar has no grammatical gender
_GENDERLESS_LANGUAGES: frozenset[str] = frozenset({
    "en", "zh", "ja", "ko", "fi", "hu", "et", "tr",
})

def get_gender(word_text: str, iso1: str) -> str:
    """
    Return the grammatical gender of *word_text*, or ``""`` for genderless
    languages and words whose gender cannot be determined.

    Gender is read from the spaCy morphological analysis of the token.  For
    nouns this is straightforward in most European languages; for verbs and
    adjectives it is returned only when the form is unambiguously inflected
    (e.g. Spanish past-participle ``"hablada"`` → ``"feminine"``).

    Args:
        word_text: Surface form, e.g. ``"Tisch"`` or ``"maison"``.
        iso1:      ISO 639-1 code, e.g. ``"de"`` or ``"fr"``.

    Returns:
        ``"m"``, ``"f"``, ``"n"``, ``"c"``, or ``""``.

    Examples:
        get_gender("Tisch",   "de")  # → "m"
        get_gender("maison",  "fr")  # → "f"
        get_gender("libro",   "es")  # → "m"
        get_gender("courir",  "fr")  # → ""   (verbs have no gender)
        get_gender("cat",     "en")  # → ""   (English has no grammatical gender)
    """
    lang = iso1.split("-")[0].lower()
    if lang in _GENDERLESS_LANGUAGES:
        return ""

    language = _LANGUAGES.get(lang)
    if language is None:
        logger.debug("get_gender: no spaCy model for iso1=%r", iso1)
        return ""

    try:
        nlp = load_spacy_model(language.spacy_model)
        doc = nlp(word_text)
        if not doc:
            return ""

        for token in doc:
            if token.pos_ in ("SPACE", "PUNCT", ""):
                continue
            gender_values = token.morph.get("Gender")   # e.g. ["Masc"]
            if gender_values:
                return _SPACY_GENDER_TO_STR.get(gender_values[0], "")
            # Gender not encoded in morphology for this token
            return ""
        return ""

    except Exception:
        logger.exception("get_gender(%r, %r) failed", word_text, iso1)
        return ""