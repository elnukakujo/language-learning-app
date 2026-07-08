"""OCR ingestion: turn a scanned course PDF/image into review-ready candidates.

Never writes to the DB directly — extract_candidates() returns enriched
word/character candidates for the client to review and confirm through the
normal create flow (which is where dedup/conflict handling already lives).
"""
import logging
from functools import cache
from pathlib import Path

logger = logging.getLogger(__name__)

# Tesseract's language packs are ISO 639-2 codes for nearly every language this
# app supports (jpn, kor, fra, deu, ... match target_iso639_2t exactly) —
# Chinese is the one exception (tesseract splits simplified/traditional).
TESSERACT_LANG_OVERRIDES = {"zho": "chi_sim"}

# ponytail: flat cap on distinct candidates enriched per upload — each one calls
# translate()/phonetics (argos/hanzipy), so an unbounded course scan could take
# minutes. Raise this (or move enrichment to a background job) if real course
# scans routinely exceed it; logs a warning when the cap is hit so it's visible.
MAX_CANDIDATES_PER_KIND = 200


@cache
def _tesseract_lang(target_iso639_2t: str) -> str:
    return TESSERACT_LANG_OVERRIDES.get(target_iso639_2t, target_iso639_2t)


class OcrService:
    def extract_text(self, file_path: str, target_iso639_2t: str) -> str:
        """OCR a PDF or image file into raw text."""
        import pytesseract
        from PIL import Image

        lang = _tesseract_lang(target_iso639_2t)
        path = Path(file_path)

        if path.suffix.lower() == ".pdf":
            import pypdfium2 as pdfium

            pdf = pdfium.PdfDocument(str(path))
            try:
                pages_text = []
                for page in pdf:
                    bitmap = page.render(scale=300 / 72)  # ~300 DPI for legible OCR
                    pages_text.append(pytesseract.image_to_string(bitmap.to_pil(), lang=lang))
                return "\n".join(pages_text)
            finally:
                pdf.close()

        return pytesseract.image_to_string(Image.open(path), lang=lang)

    def extract_candidates(self, file_path: str, language) -> dict:
        """OCR the file, then enrich distinct words/characters found in it.

        Args:
            file_path: Path to the uploaded course scan (PDF or image).
            language: The Language row the import targets (for iso codes / spacy model).

        Returns:
            {
              "text": "<raw OCR text>",
              "words": [{"word": ..., "translation": ..., "phonetic": ..., ...}],
              "characters": [{"character": ..., "meaning": ..., "phonetic": ..., ...}],
              "truncated": bool,
            }
        """
        from ..utils import (
            enrich_character,
            enrich_word,
            get_characters,
            get_content_words,
            get_language_by_iso2t,
        )

        text = self.extract_text(file_path, language.target_iso639_2t)

        target_lang = get_language_by_iso2t(language.target_iso639_2t)
        source_lang = get_language_by_iso2t(language.source_iso639_2t)
        result = {"text": text, "words": [], "characters": [], "truncated": False}

        if target_lang.spacy_model == "unknown":
            logger.warning(f"No spaCy model for '{language.target_iso639_2t}'; returning raw OCR text only")
            return result

        words = get_content_words(text, target_lang.spacy_model)
        characters = get_characters(text, target_lang.spacy_model)
        result["truncated"] = len(words) > MAX_CANDIDATES_PER_KIND or len(characters) > MAX_CANDIDATES_PER_KIND
        if result["truncated"]:
            logger.warning(
                f"OCR found {len(words)} words / {len(characters)} characters; "
                f"capping enrichment at {MAX_CANDIDATES_PER_KIND} each"
            )

        for word in words[:MAX_CANDIDATES_PER_KIND]:
            enriched = enrich_word(
                word_text=word,
                source_iso1=source_lang.iso1,
                target_iso1=target_lang.iso1,
                target_spacy_model=target_lang.spacy_model,
            )
            result["words"].append({"word": word, **enriched})

        for character in characters[:MAX_CANDIDATES_PER_KIND]:
            enriched = enrich_character(
                character_text=character,
                target_iso1=target_lang.iso1,
                source_iso1=source_lang.iso1,
            )
            result["characters"].append({"character": character, **enriched})

        return result
