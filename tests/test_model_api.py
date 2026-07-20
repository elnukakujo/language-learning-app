"""Self-check for the OpenAI-compatible API helpers in lapp.utils.model_api.

Run: `uv run python tests/test_model_api.py` (no pytest needed).
"""
from unittest.mock import MagicMock, patch

import httpx

from lapp.utils.model_api import chat_completion, synthesize_speech, resolve_api


def _mock_response(json_data=None, content=b"", status_code=200):
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.json.return_value = json_data
    resp.content = content
    if status_code >= 400:
        resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "error", request=MagicMock(), response=resp
        )
    else:
        resp.raise_for_status.side_effect = None
    return resp


def test_chat_completion_extracts_message_content():
    resp = _mock_response(json_data={"choices": [{"message": {"content": "hello"}}]})
    with patch("httpx.Client.post", return_value=resp) as post:
        result = chat_completion("http://x", "key", "m", [{"role": "user", "content": "hi"}], max_tokens=10)
        assert result == "hello"
        assert post.call_args.args[0] == "/chat/completions"


def test_resolve_api_uses_override_when_present():
    default = {"base_url": "http://default", "api_key": "dkey", "model": "dmodel"}
    result = resolve_api(default, "http://override", "okey", "omodel")
    assert result == {"base_url": "http://override", "api_key": "okey", "model": "omodel"}


def test_resolve_api_falls_back_to_default_when_blank():
    default = {"base_url": "http://default", "api_key": "dkey", "model": "dmodel"}
    result = resolve_api(default, None, "", None)
    assert result == default


def test_synthesize_speech_returns_bytes():
    resp = _mock_response(content=b"wav-audio-bytes")
    with patch("httpx.Client.post", return_value=resp):
        result = synthesize_speech("http://x", "key", "m", "hello world")
        assert result == b"wav-audio-bytes"


def test_error_response_raises():
    resp = _mock_response(status_code=500)
    with patch("httpx.Client.post", return_value=resp):
        try:
            chat_completion("http://x", "key", "m", [], max_tokens=10)
        except httpx.HTTPStatusError:
            pass
        else:
            raise AssertionError("expected HTTPStatusError to propagate")


if __name__ == "__main__":
    test_chat_completion_extracts_message_content()
    test_resolve_api_uses_override_when_present()
    test_resolve_api_falls_back_to_default_when_blank()
    test_synthesize_speech_returns_bytes()
    test_error_response_raises()
    print("OK")
