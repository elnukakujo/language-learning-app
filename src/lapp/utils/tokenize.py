import logging
logger = logging.getLogger(__name__)

def tokenize(
    text: str,
    spacy_model_id: str,
    *,
    include_punct: bool = False,
    lemmatize: bool = True,
) -> list[dict]:
    """
    Split *text* into tokens using the appropriate spaCy model.
 
    Handles space-free scripts (Chinese, Japanese, Korean) via the bundled
    statistical segmenters in zh_core_web_md / ja_core_news_md /
    ko_core_news_sm. All other languages use whitespace + rule-based splitting.
 
    Args:
        text:          Raw passage / sentence text.
        spacy_model_id:  spaCy model identifier.
        include_punct: Keep punctuation tokens if True.
        lemmatize:     Use lemma form in "lemma" key if True.
 
    Returns:
        List of dicts: [{"text": str, "lemma": str, "is_punct": bool}, ...]
 
    Example (Chinese):
        tokenize("我喜欢学习汉语", "zh")
        # → [
        #     {"text": "我",   "lemma": "我",   "is_punct": False},
        #     {"text": "喜欢", "lemma": "喜欢", "is_punct": False},
        #     {"text": "学习", "lemma": "学习", "is_punct": False},
        #     {"text": "汉语", "lemma": "汉语", "is_punct": False},
        #   ]
    """
    from .spacy_model import load_spacy_model

    nlp = load_spacy_model(spacy_model_id)
    doc = nlp(text)
 
    tokens = []
    for tok in doc:
        if tok.is_space:
            continue
        if not include_punct and tok.is_punct:
            continue
        tokens.append({
            "text":     tok.text,
            "lemma":    tok.lemma_ if lemmatize else tok.text,
            "is_punct": tok.is_punct,
        })
    return tokens

def get_content_words(text: str, spacy_model_id: str) -> list[str]:
    """
    Return only meaningful word lemmas (no punctuation or whitespace).
    Convenience wrapper around tokenize(); use for DB junction-table population.
 
    Examples:
        get_content_words("我喜欢学习汉语", "zh")
        # → ["我", "喜欢", "学习", "汉语"]
 
        get_content_words("The cats are running fast.", "en")
        # → ["cat", "be", "run", "fast"]   (lemmatised)
    """
    return [t["lemma"] for t in tokenize(text, spacy_model_id) if not t["is_punct"]]
 
 
def get_characters(text: str, spacy_model_id: str) -> list[str]:
    """
    Return individual characters from *text*, deduplicated and order-preserved.
 
    For CJK, tokens are flattened to individual Unicode code points (the
    "Character" DB entity). For Latin-script languages each letter is returned
    — useful if you track calligraphy for Greek, Russian, Ukrainian, etc.
 
    Examples:
        get_characters("你好世界", "zh")  # → ["你", "好", "世", "界"]
        get_characters("café",    "fr")  # → ["c", "a", "f", "é"]
        get_characters("Привет",  "ru")  # → ["П", "р", "и", "в", "е", "т"]
    """
    seen: set[str] = set()
    result: list[str] = []
    for word in get_content_words(text, spacy_model_id):
        for ch in word:
            if ch not in seen and not ch.isspace():
                seen.add(ch)
                result.append(ch)
    return result