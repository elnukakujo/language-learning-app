import logging
from functools import lru_cache
from typing import Optional

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def _hanzi_dict():
    from hanzipy.dictionary import HanziDictionary
    return HanziDictionary()
 
@lru_cache(maxsize=1)
def _hanzi_decomposer():
    from hanzipy.decomposer import HanziDecomposer
    return HanziDecomposer()
 
 
def get_cjk_character_info(character: str, iso1: str) -> dict:
    """
    Return radical, stroke count, and English meaning for a single CJK character.
 
    Relevant for: zh (Chinese), ja (Japanese kanji).
    Returns empty values for all other languages.
 
    Args:
        character: A single character string, e.g. "学".
        iso1:      ISO 639-1 language code.
 
    Returns:
        {
          "radical": str,        # e.g. "子" — Kangxi radical; "" if unknown
          "strokes": int | None, # total stroke count; None if unknown
          "meaning": str,        # English gloss (CEDICT first sense); "" if unknown
        }
 
    Examples:
        get_cjk_character_info("学", "zh")
        # → {"radical": "子", "strokes": 8, "meaning": "to learn"}
 
        get_cjk_character_info("水", "ja")
        # → {"radical": "水", "strokes": 4, "meaning": "water"}
 
        get_cjk_character_info("A", "en")
        # → {"radical": "", "strokes": None, "meaning": ""}
    """
    empty: dict = {"radical": "", "strokes": None, "meaning": ""}
    lang = iso1.split("-")[0].lower()
 
    if lang not in ("zh", "ja"):
        return empty
 
    try:
        # --- radical ---
        radical = ""
        try:
            decomposition = _hanzi_decomposer().decompose(character)
            radical_list = decomposition.get("radical", [])
            valid = [r for r in radical_list if "glyph" not in r.lower()]
            radical = valid[0] if valid else ""
        except Exception:
            pass
 
        # --- stroke count + meaning (both from CEDICT via hanzipy) ---
        strokes: Optional[int] = None
        meaning = ""
        try:
            entries = _hanzi_dict().definition_lookup(character, script_type="simplified")
            if entries:
                entry = entries[0]
                raw_strokes = entry.get("strokeCount") or entry.get("stroke_count")
                if raw_strokes is not None:
                    strokes = int(raw_strokes)
                defs = entry.get("definition", "")
                if defs:
                    meaning = defs.split(" /")[0].strip(" /")
        except Exception:
            pass
 
        return {"radical": radical, "strokes": strokes, "meaning": meaning}
 
    except Exception as exc:
        logger.error("get_cjk_character_info(%r, %s): %s", character, iso1, exc)
        return empty