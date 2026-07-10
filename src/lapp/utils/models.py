import logging
from pathlib import Path

from .offline import configure_offline_environment

logger = logging.getLogger(__name__)

OFFLINE = configure_offline_environment()


def _resolve_local_hf_snapshot(model_repo_name: str) -> str | None:
    cache_root = Path.home() / ".cache" / "huggingface" / "hub"
    repo_dir = cache_root / f"models--{model_repo_name.replace('/', '--')}"
    snapshots_dir = repo_dir / "snapshots"

    if not snapshots_dir.exists():
        return None

    snapshots = sorted(p for p in snapshots_dir.iterdir() if p.is_dir())
    if not snapshots:
        return None

    return str(snapshots[-1])

from functools import cache


@cache
def get_text_embedding_model():
    """Text-to-representation model (clustering, retrieval, similarity)."""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2", local_files_only=OFFLINE)


@cache
def get_audio_embedding_model():
    from transformers import Wav2Vec2Model
    return Wav2Vec2Model.from_pretrained(
        "facebook/wav2vec2-large-xlsr-53", local_files_only=OFFLINE
    )


@cache
def get_audio_embedding_processor():
    from transformers import Wav2Vec2FeatureExtractor
    return Wav2Vec2FeatureExtractor.from_pretrained(
        "facebook/wav2vec2-large-xlsr-53", local_files_only=OFFLINE
    )


@cache
def get_stt_pipe():
    """Speech-to-text pipeline (Whisper-medium)."""
    import torch
    from transformers import (
        AutoModelForSpeechSeq2Seq,
        AutoProcessor,
        pipeline,
    )
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        "openai/whisper-medium",
        dtype=torch.float16,
        use_safetensors=True,
        local_files_only=OFFLINE,
    )
    processor = AutoProcessor.from_pretrained(
        "openai/whisper-medium", local_files_only=OFFLINE
    )
    return pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        dtype=torch.float16,
    )


@cache
def get_qwen_tts_model():
    """Text-to-speech model (Qwen3-TTS)."""
    import torch
    from qwen_tts import Qwen3TTSModel
    path = _resolve_local_hf_snapshot("Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice")
    return Qwen3TTSModel.from_pretrained(
        path or "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
        device_map="cpu",
        dtype=torch.bfloat16,
        local_files_only=OFFLINE,
    )


@cache
def get_text_gen_tokenizer():
    from transformers import AutoTokenizer
    path = _resolve_local_hf_snapshot("Qwen/Qwen2.5-1.5B-Instruct")
    return AutoTokenizer.from_pretrained(
        path or "Qwen/Qwen2.5-1.5B-Instruct", local_files_only=OFFLINE
    )


@cache
def get_text_gen_model():
    """Text generation model (Qwen2.5-1.5B-Instruct)."""
    from transformers import AutoModelForCausalLM
    path = _resolve_local_hf_snapshot("Qwen/Qwen2.5-1.5B-Instruct")
    return AutoModelForCausalLM.from_pretrained(
        path or "Qwen/Qwen2.5-1.5B-Instruct",
        device_map="auto",
        dtype="auto",
        local_files_only=OFFLINE,
    )