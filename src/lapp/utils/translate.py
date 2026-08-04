import logging
import threading

import argostranslate.package
import argostranslate.translate

logger = logging.getLogger(__name__)

# One lock per language pair so concurrent requests for the same pair
# don't trigger duplicate downloads.
_install_locks: dict[str, threading.Lock] = {}
_install_locks_mutex = threading.Lock()


def _get_install_lock(key: str) -> threading.Lock:
    with _install_locks_mutex:
        if key not in _install_locks:
            _install_locks[key] = threading.Lock()
        return _install_locks[key]


def _ensure_argos_pair(source_iso1: str, target_iso1: str) -> None:
    """
    Download and install the argostranslate package for *source_iso1* → *target_iso1*
    if it is not already present.  No-ops when the pair is already installed.
    Thread-safe: concurrent calls for the same pair serialise on a per-pair lock
    so the package is only downloaded once.
    """
    lock_key = f"{source_iso1}→{target_iso1}"
    with _get_install_lock(lock_key):
        # Re-check inside the lock — another thread may have installed it.
        installed = argostranslate.translate.get_installed_languages()
        codes = {l.code for l in installed}
        if source_iso1 in codes and target_iso1 in codes:
            src_lang = next(l for l in installed if l.code == source_iso1)
            if src_lang.get_translation(
                next(l for l in installed if l.code == target_iso1)
            ) is not None:
                return  # already good

        logger.info(
            "argostranslate: package %s→%s not found — downloading now",
            source_iso1, target_iso1,
        )
        argostranslate.package.update_package_index()
        available = argostranslate.package.get_available_packages()

        pkg = next(
            (
                p for p in available
                if p.from_code == source_iso1 and p.to_code == target_iso1
            ),
            None,
        )
        if pkg is None:
            raise RuntimeError(
                f"argostranslate: no package available for {source_iso1!r}→{target_iso1!r}. "
                "Check https://www.argosopentech.com/argospm/index/ for supported pairs."
            )

        logger.info("argostranslate: installing %s", pkg)
        argostranslate.package.install_from_path(pkg.download())
        logger.info("argostranslate: installed %s→%s", source_iso1, target_iso1)


def _get_argos_translator(source_iso1: str, target_iso1: str):
    """Return an argostranslate ITranslation, installing the package on demand."""
    _ensure_argos_pair(source_iso1, target_iso1)

    installed = argostranslate.translate.get_installed_languages()
    src_lang = next((l for l in installed if l.code == source_iso1), None)
    tgt_lang = next((l for l in installed if l.code == target_iso1), None)

    if src_lang is None or tgt_lang is None:
        # Should never happen after _ensure_argos_pair succeeded.
        raise RuntimeError(
            f"argostranslate: language(s) still missing after install: "
            f"{source_iso1!r}→{target_iso1!r}"
        )

    translator = src_lang.get_translation(tgt_lang)
    if translator is None:
        raise RuntimeError(
            f"argostranslate: no translation path {source_iso1!r}→{target_iso1!r} "
            "after install. The package index may be incomplete."
        )
    return translator


def translate(text: str, source_iso1: str, target_iso1: str = "en") -> str:
    """
    Translate *text* fully in-process using argostranslate (OpenNMT models).
    Packages are downloaded and installed automatically on first use — no
    manual setup step required.

    Args:
        text:        Text to translate.
        source_iso1: ISO 639-1 source language code, e.g. "zh".
        target_iso1: ISO 639-1 target language code, e.g. "en".

    Returns:
        Translated string, or the original *text* on failure.
    """
    if source_iso1 == target_iso1:
        return text
    try:
        return _get_argos_translator(source_iso1, target_iso1).translate(text)
    except Exception as exc:
        logger.error("translate(%r, %s→%s): %s", text, source_iso1, target_iso1, exc)
        return text