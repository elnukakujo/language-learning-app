def get_phonetic(text: str, iso1: str) -> str:
    """
    Return a romanised / phonetic transcription of *text*.
 
    Language    Library             Output style
    ----------  ------------------  ----------------------------
    zh          pypinyin            Pinyin with tone marks
    ja          pykakasi            Hepburn romanisation
    ko          hangul-romanize     Revised Romanisation
    others      —                   "" (Latin-script: no transcription needed)
 
    Extend the elif chain below to support Arabic, Hindi, Thai, etc. if you
    add those spaCy models later.
 
    Args:
        text:  Surface text, e.g. "北京" or "東京".
        iso1:  ISO 639-1 code.
 
    Returns:
        Phonetic string, or "" for languages that need no transcription.
 
    Examples:
        get_phonetic("北京",    "zh")  # → "běi jīng"
        get_phonetic("東京",    "ja")  # → "toukyou"
        get_phonetic("한국어",  "ko")  # → "hangugeo"
        get_phonetic("Bonjour", "fr")  # → ""
    """
    lang = iso1.split("-")[0].lower()
 
    if lang == "zh":
        from pypinyin import pinyin, Style
        syllables = pinyin(text, style=Style.TONE)
        return " ".join(s[0] for s in syllables if s)
 
    if lang == "ja":
        import pykakasi
        result = pykakasi.kakasi().convert(text)
        return "".join(item["hepburn"] for item in result)
 
    if lang == "ko":
        from hangul_romanize import Transliter
        from hangul_romanize.rule import RevisedRomanisation
        return Transliter(RevisedRomanisation).translit(text)
 
    return ""