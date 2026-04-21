from .phonetics import get_phonetic
from .strokes import get_cjk_character_info
from .tokenize import get_content_words, get_characters
from .translate import translate

def enrich_character(character_text: str, iso1: str, native_iso1: str) -> dict:
    """
    Compute all storable fields for a Character DB entity.
 
    For CJK (zh/ja) this queries hanzipy for radical, stroke count, and an
    English gloss, then translates the gloss to the learner's language.
    For other scripts only phonetic (if applicable) and a direct translation
    are returned; radical and strokes are left empty/None.
 
    Args:
        character_text: Single character, e.g. "北" or "Ω".
        iso1:           Language ISO code,       e.g. "zh".
        native_iso1:    Learner's native language, e.g. "fr".
 
    Returns:
        {
          "phonetic": "běi",
          "radical":  "匕",         # "" for non-CJK
          "strokes":  5,            # None for non-CJK
          "meaning":  "nord",       # translated into native_iso1
        }
    """
    cjk = get_cjk_character_info(character_text, iso1)
 
    if cjk["meaning"]:
        # Translate CEDICT English gloss → learner's language
        meaning = (
            translate(cjk["meaning"], "en", native_iso1)
            if native_iso1 != "en"
            else cjk["meaning"]
        )
    else:
        # Non-CJK or unknown: translate the character itself
        meaning = translate(character_text, iso1, native_iso1)
 
    return {
        "phonetic": get_phonetic(character_text, iso1),
        "radical":  cjk["radical"],
        "strokes":  cjk["strokes"],
        "meaning":  meaning,
    }
 
 
def enrich_word(word_text: str, iso1: str, native_iso1: str) -> dict:
    """
    Compute all storable fields for a Word DB entity.
 
    Args:
        word_text:   The word, e.g. "北京" or "courir".
        iso1:        Language of the word, e.g. "zh".
        native_iso1: Learner's native language, e.g. "en".
 
    Returns:
        {
          "phonetic":    "běi jīng",   # "" for Latin-script languages
          "translation": "Beijing",
        }
    """
    return {
        "phonetic":    get_phonetic(word_text, iso1),
        "translation": translate(word_text, iso1, native_iso1),
    }
 
 
def enrich_passage(passage_text: str, iso1: str, native_iso1: str) -> dict:
    """
    Compute all storable fields for a Passage DB entity and return the token
    lists needed to populate passage_word and passage_character junction tables.
 
    Args:
        passage_text: Full passage text.
        iso1:         Language of the passage.
        native_iso1:  Learner's native language.
 
    Returns:
        {
          "translation": str,
          "words":       list[str],  # lemmas — match against Word table
          "characters":  list[str],  # individual chars — match against Character table
        }
    """
    return {
        "translation": translate(passage_text, iso1, native_iso1),
        "words":       get_content_words(passage_text, iso1),
        "characters":  get_characters(passage_text, iso1),
    }