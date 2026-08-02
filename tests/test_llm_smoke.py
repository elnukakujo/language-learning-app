"""Real-LLM smoke tests. Skipped unless LAPP_TEST_LLM_* env vars are set.

Run: uv run pytest tests/test_llm_smoke.py -m smoke -v
"""
import os
import pytest

from lapp.utils.model_api import chat_completion, synthesize_speech

BASE_URL = os.environ.get("LAPP_TEST_LLM_BASE_URL")
API_KEY = os.environ.get("LAPP_TEST_LLM_API_KEY")
MODEL = os.environ.get("LAPP_TEST_LLM_MODEL")
VOICE = os.environ.get("LAPP_TEST_TTS_VOICE", "alloy")

pytestmark = [
    pytest.mark.smoke,
    pytest.mark.skipif(
        not (BASE_URL and API_KEY and MODEL),
        reason="set LAPP_TEST_LLM_BASE_URL, LAPP_TEST_LLM_API_KEY, LAPP_TEST_LLM_MODEL",
    ),
]


def test_chat_completion_returns_text():
    result = chat_completion(
        BASE_URL, API_KEY, MODEL,
        [{"role": "user", "content": "Reply with exactly one word: hello"}],
        max_tokens=32,
    )
    assert isinstance(result, str) and result.strip()


def test_synthesize_speech_returns_wav():
    audio = synthesize_speech(BASE_URL, API_KEY, MODEL, "Hello there", voice=VOICE)
    assert isinstance(audio, bytes) and len(audio) > 44
    assert audio[:4] == b"RIFF" and audio[8:12] == b"WAVE"
