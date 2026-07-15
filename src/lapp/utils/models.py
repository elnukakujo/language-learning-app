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


def _resolve_local_hf_snapshot(model_repo_name: str, require_tokenizer: bool = False) -> str | None:
    """
    Find the latest cached HF snapshot for a repo, or None if it's missing/
    incomplete. `from_pretrained` treats a local directory path as fully
    offline (it never fetches missing files from the hub for a literal
    path), so handing it a snapshot that's missing files it needs is worse
    than not resolving a path at all - it fails instead of downloading.

    require_tokenizer=True is for tokenizer loads: model and tokenizer
    downloads are separate from_pretrained calls sharing the same cache dir,
    so weights can be fully cached while tokenizer files were never fetched.
    require_tokenizer=False (weights/audio models) only checks weight files.
    """
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
    latest = snapshots[-1]
    entries = sorted(p.name for p in latest.iterdir())
    weight_patterns = ("*.safetensors", "*.bin", "*.h5", "*.msgpack", "*.ckpt.index")
    weight_matches = [f for pattern in weight_patterns for f in latest.rglob(pattern)]
    has_weights = any(f.resolve().exists() for f in weight_matches)
    logger.info(f"[hf-snapshot] {model_repo_name}: latest={latest} entries={entries}")
    if not has_weights:
        logger.info(f"[hf-snapshot] {model_repo_name}: rejected, no resolvable weight files")
        return None

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
    if require_tokenizer and not tokenizer_status:
        logger.info(f"[hf-snapshot] {model_repo_name}: rejected, tokenizer files were never downloaded")
        return None

    logger.info(f"[hf-snapshot] {model_repo_name}: accepted -> {latest}")
    return str(latest)

from functools import cache


# Repo IDs are configurable per task via env vars so a different checkpoint
# can be swapped in without touching code; default to the models this file
# has always used.
TEXT_EMBEDDING_MODEL = os.environ.get("LAPP_TEXT_EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
AUDIO_EMBEDDING_MODEL = os.environ.get("LAPP_AUDIO_EMBEDDING_MODEL", "facebook/mms-300m")
STT_MODEL = os.environ.get("LAPP_STT_MODEL", "openai/whisper-large-v3-turbo")
TTS_MODEL = os.environ.get("LAPP_TTS_MODEL", "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice")
TEXT_GEN_MODEL = os.environ.get("LAPP_TEXT_GEN_MODEL", "Qwen/Qwen3-1.7B")


def _local_files_only(repo_id: str, require_tokenizer: bool = False) -> tuple[str | None, bool]:
    """Resolve a repo to a local snapshot path if fully cached, and whether
    from_pretrained should be told to stay offline. A fully cached snapshot
    means offline mode regardless of network reachability; otherwise fall
    back to the network-reachability check so a missing/partial cache still
    triggers a download when online."""
    path = _resolve_local_hf_snapshot(repo_id, require_tokenizer=require_tokenizer)
    return path, bool(path) or configure_offline_environment()


@cache
def get_text_embedding_model():
    """Text-to-representation model (clustering, retrieval, similarity)."""
    from sentence_transformers import SentenceTransformer
    path, offline = _local_files_only(TEXT_EMBEDDING_MODEL)
    return SentenceTransformer(
        path or TEXT_EMBEDDING_MODEL, device=get_device(), local_files_only=offline
    )


@cache
def get_audio_embedding_model():
    from transformers import Wav2Vec2Model
    path, offline = _local_files_only(AUDIO_EMBEDDING_MODEL)
    return Wav2Vec2Model.from_pretrained(
        path or AUDIO_EMBEDDING_MODEL, local_files_only=offline
    ).to(get_device())


@cache
def get_audio_embedding_processor():
    from transformers import Wav2Vec2FeatureExtractor
    path, offline = _local_files_only(AUDIO_EMBEDDING_MODEL, require_tokenizer=True)
    return Wav2Vec2FeatureExtractor.from_pretrained(
        path or AUDIO_EMBEDDING_MODEL, local_files_only=offline
    )


@cache
def get_stt_pipe():
    """Speech-to-text pipeline (Whisper-large-v3-turbo by default)."""
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
    path, offline = _local_files_only(STT_MODEL, require_tokenizer=True)
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        path or STT_MODEL,
        dtype=dtype,
        use_safetensors=True,
        local_files_only=offline,
    ).to(device)
    processor = AutoProcessor.from_pretrained(path or STT_MODEL, local_files_only=offline)
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
    """Text-to-speech model (Qwen3-TTS by default)."""
    import torch
    from qwen_tts import Qwen3TTSModel
    path, offline = _local_files_only(TTS_MODEL)
    device = get_device()
    # bfloat16 has no native CPU arithmetic support (esp. on Apple Silicon) and
    # falls back to slow scalar emulation, making generation 10-50x slower.
    # Real GPUs (cuda) have hardware bf16, so use it there.
    dtype = torch.bfloat16 if device == "cuda" else torch.float32
    return Qwen3TTSModel.from_pretrained(
        path or TTS_MODEL,
        device_map=device,
        dtype=dtype,
        local_files_only=offline,
    )


@cache
def get_text_gen_tokenizer():
    from transformers import AutoTokenizer
    path, offline = _local_files_only(TEXT_GEN_MODEL, require_tokenizer=True)
    logger.info(f"[text-gen-tokenizer] path={path!r} offline={offline}")
    return AutoTokenizer.from_pretrained(path or TEXT_GEN_MODEL, local_files_only=offline)


@cache
def get_text_gen_model():
    """Text generation model (Qwen3-1.7B by default)."""
    from transformers import AutoModelForCausalLM
    path, offline = _local_files_only(TEXT_GEN_MODEL)
    return AutoModelForCausalLM.from_pretrained(
        path or TEXT_GEN_MODEL,
        # device_map="auto" is for multi-GPU orchestration; on a single-device
        # box its memory heuristic can misfire and leave layers stranded on
        # the meta device (uninitialized). Pick one device explicitly instead.
        device_map=get_device(),
        dtype="auto",
        local_files_only=offline,
    )