import logging
logger = logging.getLogger(__name__)

def _get_argos_translator(source_iso1: str, target_iso1: str = "en"):
    """Return a cached argostranslate ITranslation for the given language pair."""
    import argostranslate.translate
 
    installed = argostranslate.translate.get_installed_languages()
    src_lang = next((l for l in installed if l.code == source_iso1), None)
    tgt_lang = next((l for l in installed if l.code == target_iso1), None)
 
    if src_lang is None or tgt_lang is None:
        missing = [c for c, l in [(source_iso1, src_lang), (target_iso1, tgt_lang)] if l is None]
        raise RuntimeError(
            f"argostranslate: language model(s) not installed: {missing}. "
            "Run `python -m lapp.setup_argos` to download them."
        )
 
    translator = src_lang.get_translation(tgt_lang)
    if translator is None:
        raise RuntimeError(
            f"argostranslate: no translation path {source_iso1!r}→{target_iso1!r}. "
            "Install more language packages."
        )
    return translator
 
 
def translate(text: str, source_iso1: str, target_iso1: str = "en") -> str:
    """
    Translate *text* fully in-process using argostranslate (OpenNMT models).
    No external server required — models run locally after one-time download.
 
    Argostranslate pivots automatically through English when a direct pair is
    not installed (e.g. zh→fr goes zh→en→fr).
 
    Args:
        text:        Text to translate.
        source_iso1: ISO 639-1 source language code, e.g. "zh".
        target_iso1: ISO 639-1 target language code, e.g. "en".
 
    Returns:
        Translated string, or the original text on failure.
 
    Examples:
        translate("你好",    "zh", "en")  # → "Hello"
        translate("Bonjour", "fr", "en")  # → "Hello"
        translate("走る",    "ja", "fr")  # → "courir"  (pivots via en)
    """
    if source_iso1 == target_iso1:
        return text
    try:
        return _get_argos_translator(source_iso1, target_iso1).translate(text)
    except Exception as exc:
        logger.error("translate(%r, %s→%s): %s", text, source_iso1, target_iso1, exc)
        return text