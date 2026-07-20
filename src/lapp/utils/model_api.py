"""HTTP client for API-backed model tasks (text-gen, feedback, TTS).

Targets the OpenAI-compatible surface shared by llama.cpp server, ollama,
OpenAI, and OpenAI-compatible proxies for other providers (Anthropic,
DeepSeek, Kimi, ...) - one client, no per-provider abstraction needed.
"""
import os

import httpx

TEXT_GEN_API = dict(
    base_url=os.environ.get("LAPP_TEXT_GEN_API_BASE_URL", ""),
    api_key=os.environ.get("LAPP_TEXT_GEN_API_KEY", ""),
    model=os.environ.get("LAPP_TEXT_GEN_MODEL", ""),
)
FEEDBACK_API = dict(
    base_url=os.environ.get("LAPP_FEEDBACK_API_BASE_URL", ""),
    api_key=os.environ.get("LAPP_FEEDBACK_API_KEY", ""),
    model=os.environ.get("LAPP_FEEDBACK_MODEL", ""),
)
TTS_API = dict(
    base_url=os.environ.get("LAPP_TTS_API_BASE_URL", ""),
    api_key=os.environ.get("LAPP_TTS_API_KEY", ""),
    model=os.environ.get("LAPP_TTS_MODEL", ""),
)


def resolve_api(default: dict, base_url: str | None, api_key: str | None, model: str | None) -> dict:
    """Merge a per-user override on top of the server's env-configured default;
    a blank/None override field falls back to the default."""
    return dict(
        base_url=base_url or default["base_url"],
        api_key=api_key or default["api_key"],
        model=model or default["model"],
    )


def _client(base_url: str, api_key: str) -> httpx.Client:
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    return httpx.Client(base_url=base_url, headers=headers, timeout=60)


def chat_completion(
    base_url: str,
    api_key: str,
    model: str,
    messages: list[dict],
    max_tokens: int,
    temperature: float = 0.4,
    top_p: float = 0.9,
) -> str:
    with _client(base_url, api_key) as client:
        resp = client.post(
            "/chat/completions",
            json={
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
            },
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


def synthesize_speech(
    base_url: str,
    api_key: str,
    model: str,
    text: str,
    voice: str = "alloy",
) -> bytes:
    with _client(base_url, api_key) as client:
        resp = client.post(
            "/audio/speech",
            json={
                "model": model,
                "input": text,
                "voice": voice,
                "response_format": "wav",
            },
        )
        resp.raise_for_status()
        return resp.content
