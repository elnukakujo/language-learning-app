import logging
logger = logging.getLogger(__name__)

def tokenize(
    text: str,
    spacy_model_id: str,
    *,
    include_punct: bool = False,
    lemmatize: bool = True,
) -> list[dict]:
    from .spacy_model import load_spacy_model
    nlp = load_spacy_model(spacy_model_id)
    doc = nlp(text)
    tokens = []
    for tok in doc:
        if tok.is_space or tok.is_punct and not include_punct:
            continue
        text_form = tok.text.strip()
        if not text_form:
            continue
        lemma = (tok.lemma_ or tok.text).strip()  # fallback to raw text if lemma is empty
        if not lemma:
            continue
        tokens.append({
            "text":     text_form,
            "lemma":    lemma if lemmatize else text_form,
            "is_punct": tok.is_punct,
        })
    return tokens


def get_content_words(text: str, spacy_model_id: str) -> list[str]:
    return [t["lemma"] for t in tokenize(text, spacy_model_id) if not t["is_punct"]]


def get_characters(text: str, spacy_model_id: str) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for word in get_content_words(text, spacy_model_id):
        for ch in word:
            if ch not in seen and not ch.isspace():
                seen.add(ch)
                result.append(ch)
    return result