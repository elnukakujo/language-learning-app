import logging
import os
from pathlib import Path

from .offline import configure_offline_environment

logger = logging.getLogger(__name__)

# torch defaults to using every CPU core for inference, which starves the rest
# of the machine (including this same process's own request handling) during
# generation. Cap it, leaving a couple cores free.
try:
    import torch
    torch.set_num_threads(max(1, (os.cpu_count() or 4) - 2))
except ImportError:
    pass


def get_device() -> str:
    """Pick the compute device: LAPP_DEVICE env var overrides, else the best
    available (cuda > mps > cpu)."""
    override = os.environ.get("LAPP_DEVICE")
    if override:
        return override
    import torch
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def _resolve_local_hf_snapshot(model_repo_name: str) -> str | None:
    cache_root = Path.home() / ".cache" / "huggingface" / "hub"
    repo_dir = cache_root / f"models--{model_repo_name.replace('/', '--')}"
    snapshots_dir = repo_dir / "snapshots"

    if not snapshots_dir.exists():
        logger.info(f"[hf-snapshot] {model_repo_name}: no snapshots dir at {snapshots_dir}")
        return None

    snapshots = sorted(p for p in snapshots_dir.iterdir() if p.is_dir())
    if not snapshots:
        logger.info(f"[hf-snapshot] {model_repo_name}: snapshots dir empty at {snapshots_dir}")
        return None

    # Weight files in the HF cache are symlinks into blobs/; an interrupted
    # download leaves the snapshot dir present but its symlinks dangling.
    # Treat that as "not cached" so callers fall back to a fresh download
    # instead of a hard local_files_only failure.
    latest = snapshots[-1]
    entries = sorted(p.name for p in latest.iterdir())
    weight_patterns = ("*.safetensors", "*.bin", "*.h5", "*.msgpack", "*.ckpt.index")
    weight_matches = [f for pattern in weight_patterns for f in latest.rglob(pattern)]
    has_weights = any(f.resolve().exists() for f in weight_matches)
    logger.info(
        f"[hf-snapshot] {model_repo_name}: latest={latest} entries={entries} "
        f"weight_matches={[(str(f), f.is_symlink(), f.resolve().exists()) for f in weight_matches]}"
    )
    if not has_weights:
        logger.info(f"[hf-snapshot] {model_repo_name}: rejected, no resolvable weight files")
        return None

    # Same dangling-symlink risk applies to tokenizer files: weights can
    # download fully while vocab.json/tokenizer.json are still missing.
    # Only treat a *present-but-broken* tokenizer symlink as incomplete;
    # a model with no tokenizer files at all (e.g. a pure audio model) is fine.
    tokenizer_names = ("tokenizer.json", "vocab.json", "merges.txt", "vocab.txt")
    tokenizer_status = {
        name: ((latest / name).is_symlink(), (latest / name).resolve().exists())
        for name in tokenizer_names
        if (latest / name).exists() or (latest / name).is_symlink()
    }
    logger.info(f"[hf-snapshot] {model_repo_name}: tokenizer_status={tokenizer_status}")
    has_dangling_tokenizer_file = any(
        is_symlink and not resolves for is_symlink, resolves in tokenizer_status.values()
    )
    if has_dangling_tokenizer_file:
        logger.info(f"[hf-snapshot] {model_repo_name}: rejected, dangling tokenizer symlink")
        return None

    logger.info(f"[hf-snapshot] {model_repo_name}: accepted -> {latest}")
    return str(latest)

from functools import cache


@cache
def get_text_embedding_model():
    """Text-to-representation model (clustering, retrieval, similarity)."""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(
        "all-MiniLM-L6-v2", device=get_device(), local_files_only=configure_offline_environment()
    )


@cache
def get_audio_embedding_model():
    from transformers import Wav2Vec2Model
    return Wav2Vec2Model.from_pretrained(
        "facebook/wav2vec2-large-xlsr-53", local_files_only=configure_offline_environment()
    ).to(get_device())


@cache
def get_audio_embedding_processor():
    from transformers import Wav2Vec2FeatureExtractor
    return Wav2Vec2FeatureExtractor.from_pretrained(
        "facebook/wav2vec2-large-xlsr-53", local_files_only=configure_offline_environment()
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
    device = get_device()
    # float16 has no native CPU arithmetic support and falls back to slow
    # scalar emulation; only use it on a real GPU.
    dtype = torch.float16 if device in ("cuda", "mps") else torch.float32
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        "openai/whisper-medium",
        dtype=dtype,
        use_safetensors=True,
        local_files_only=configure_offline_environment(),
    ).to(device)
    processor = AutoProcessor.from_pretrained(
        "openai/whisper-medium", local_files_only=configure_offline_environment()
    )
    return pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        dtype=dtype,
        device=device,
    )


@cache
def get_qwen_tts_model():
    """Text-to-speech model (Qwen3-TTS)."""
    import torch
    from qwen_tts import Qwen3TTSModel
    path = _resolve_local_hf_snapshot("Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice")
    device = get_device()
    # bfloat16 has no native CPU arithmetic support (esp. on Apple Silicon) and
    # falls back to slow scalar emulation, making generation 10-50x slower.
    # Real GPUs (cuda) have hardware bf16, so use it there.
    dtype = torch.bfloat16 if device == "cuda" else torch.float32
    return Qwen3TTSModel.from_pretrained(
        path or "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
        device_map=device,
        dtype=dtype,
        local_files_only=configure_offline_environment(),
    )


@cache
def get_text_gen_tokenizer():
    from transformers import AutoTokenizer
    path = _resolve_local_hf_snapshot("Qwen/Qwen2.5-1.5B-Instruct")
    offline = configure_offline_environment()
    logger.info(f"[text-gen-tokenizer] path={path!r} offline={offline}")
    return AutoTokenizer.from_pretrained(
        path or "Qwen/Qwen2.5-1.5B-Instruct", local_files_only=offline
    )


@cache
def get_text_gen_model():
    """Text generation model (Qwen2.5-1.5B-Instruct)."""
    from transformers import AutoModelForCausalLM
    path = _resolve_local_hf_snapshot("Qwen/Qwen2.5-1.5B-Instruct")
    return AutoModelForCausalLM.from_pretrained(
        path or "Qwen/Qwen2.5-1.5B-Instruct",
        # device_map="auto" is for multi-GPU orchestration; on a single-device
        # box its memory heuristic can misfire and leave layers stranded on
        # the meta device (uninitialized). Pick one device explicitly instead.
        device_map=get_device(),
        dtype="auto",
        local_files_only=configure_offline_environment(),
    )