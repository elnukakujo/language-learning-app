"""HTTP client for API-backed model tasks (text-gen, feedback, TTS).

Targets the OpenAI-compatible surface shared by llama.cpp server, ollama,
OpenAI, and OpenAI-compatible proxies for other providers (Anthropic,
DeepSeek, Kimi, ...) - one client, no per-provider abstraction needed.

There is no server-wide default for these - each user configures their own
API (base_url/api_key/model) in Settings; a task is simply skipped when a
user hasn't configured one (see the `if not api["base_url"]` guards at each
call site).
"""
import httpx


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
    model: str = "",
    text: str = "",
    voice: str = "alloy",
) -> bytes:
    body: dict = {"input": text, "voice": voice}
    if model:
        body["model"] = model
    # ponytail: only include response_format when model is present (OpenAI path);
    # Custom providers like Kokoro don't expect it.
    if model:
        body["response_format"] = "wav"
    with _client(base_url, api_key) as client:
        resp = client.post("/audio/speech", json=body)
        resp.raise_for_status()
        return resp.content
