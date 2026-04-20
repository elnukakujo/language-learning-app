from langdetect import detect
import whisper
import os
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Language:
    iso1:        str   # ISO 639-1       e.g. "fr"
    iso2t:       str   # ISO 639-2/T     e.g. "fra"
    spacy_model: str   # spaCy model     e.g. "fr_core_news_sm"
    name:        str   # English name    e.g. "French"

_LANGUAGES: dict[str, Language] = {
    "ca": Language("ca", "cat", "ca_core_news_md",  "Catalan"),
    "zh": Language("zh", "zho", "zh_core_web_md",   "Chinese"),
    "hr": Language("hr", "hrv", "hr_core_news_md",  "Croatian"),
    "da": Language("da", "dan", "da_core_news_md",  "Danish"),
    "nl": Language("nl", "nld", "nl_core_news_md",  "Dutch"),
    "en": Language("en", "eng", "en_core_web_md",   "English"),
    "fi": Language("fi", "fin", "fi_core_news_md",  "Finnish"),
    "fr": Language("fr", "fra", "fr_core_news_md",  "French"),
    "de": Language("de", "deu", "de_core_news_md",  "German"),
    "el": Language("el", "ell", "el_core_news_md",  "Greek"),
    "it": Language("it", "ita", "it_core_news_md",  "Italian"),
    "ja": Language("ja", "jpn", "ja_core_news_md",  "Japanese"),
    "ko": Language("ko", "kor", "ko_core_news_sm",  "Korean"),
    "lt": Language("lt", "lit", "lt_core_news_md",  "Lithuanian"),
    "mk": Language("mk", "mkd", "mk_core_news_md",  "Macedonian"),
    "nb": Language("nb", "nob", "nb_core_news_md",  "Norwegian Bokmål"),
    "no": Language("no", "nor", "nb_core_news_md",  "Norwegian"),
    "pl": Language("pl", "pol", "pl_core_news_md",  "Polish"),
    "pt": Language("pt", "por", "pt_core_news_md",  "Portuguese"),
    "ro": Language("ro", "ron", "ro_core_news_md",  "Romanian"),
    "ru": Language("ru", "rus", "ru_core_news_md",  "Russian"),
    "sl": Language("sl", "slv", "sl_core_news_md",  "Slovenian"),
    "es": Language("es", "spa", "es_core_news_md",  "Spanish"),
    "sv": Language("sv", "swe", "sv_core_news_md",  "Swedish"),
    "uk": Language("uk", "ukr", "uk_core_news_md",  "Ukrainian"),
}

_UNKNOWN = Language("unknown", "unknown", "unknown", "Unknown")

def _lookup(iso1: str) -> Language:
    # langdetect sometimes returns "zh-cn" / "zh-tw" — normalise to bare code
    return _LANGUAGES.get(iso1.split("-")[0], _UNKNOWN)

audio_detection_model = whisper.load_model("base")

def detect_text_language(text: str) -> Language:
    """
    Detect the language of a text string.

    Returns a Language dataclass with iso1, iso2t, spacy_model, and name.
    Falls back to Language("unknown", ...) on error.

    Example:
        lang = detect_text_language("Bonjour le monde")
        lang.iso1        # "fr"
        lang.iso2t       # "fra"
        lang.spacy_model # "fr_core_news_sm"
        lang.name        # "French"
    """
    try:
        lang = _lookup(detect(text))
        logger.debug(f"Detected text language: {lang}")
        return lang
    except Exception as e:
        logger.error(f"Error detecting text language: {e}")
        return _UNKNOWN


def detect_audio_language(audio_file_path: str) -> tuple[Language, float]:
    """
    Detect the language of an audio file using Whisper.

    Returns (Language, confidence) or (_UNKNOWN, 0.0) on error.

    Example:
        lang, confidence = detect_audio_language("clip.mp3")
        lang.iso2t   # "fra"
        confidence   # 0.97
    """
    try:
        if not os.path.isfile(audio_file_path):
            logger.error(f"Audio file does not exist: {audio_file_path}")
            return _UNKNOWN, 0.0

        audio = whisper.load_audio(audio_file_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(
            audio, n_mels=audio_detection_model.dims.n_mels
        ).to(audio_detection_model.device)

        _, probs = audio_detection_model.detect_language(mel)
        iso1 = max(probs, key=probs.get)
        confidence = probs[iso1]

        lang = _lookup(iso1)
        logger.debug(f"Detected audio language: {lang} (confidence: {confidence:.2f})")
        return lang, confidence

    except Exception as e:
        logger.error(f"Error detecting audio language: {e}")
        return _UNKNOWN, 0.0