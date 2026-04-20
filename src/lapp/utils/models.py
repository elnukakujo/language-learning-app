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

import torch
import whisper
from sentence_transformers import SentenceTransformer
from transformers import (
    AutoModelForCausalLM,
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    AutoTokenizer,
    Wav2Vec2FeatureExtractor,
    Wav2Vec2Model,
    pipeline,
)
from qwen_tts import Qwen3TTSModel

# Text-to-representation model (for clustering, retrieval, etc.)
text_embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    local_files_only=OFFLINE,
)

# Audio-to-representation model (for clustering, retrieval, etc.)
audio_embedding_model = Wav2Vec2Model.from_pretrained(
    "facebook/wav2vec2-large-xlsr-53",
    local_files_only=OFFLINE,
)
audio_embedding_processor = Wav2Vec2FeatureExtractor.from_pretrained(
    "facebook/wav2vec2-large-xlsr-53",
    local_files_only=OFFLINE,
)

# Speech-to-text model
stt_model = AutoModelForSpeechSeq2Seq.from_pretrained(
    "openai/whisper-medium",
    dtype=torch.float16,
    use_safetensors=True,
    local_files_only=OFFLINE,
)
stt_processor = AutoProcessor.from_pretrained(
    "openai/whisper-medium",
    local_files_only=OFFLINE,
)
stt_pipe = pipeline(
    "automatic-speech-recognition",
    model=stt_model,
    tokenizer=stt_processor.tokenizer,
    feature_extractor=stt_processor.feature_extractor,
    dtype=torch.float16,
)

# Text-to-speech model
qwen_tts_model_path = _resolve_local_hf_snapshot("Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice")
qwen_tts_model = Qwen3TTSModel.from_pretrained(
    qwen_tts_model_path or "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
    device_map="cpu",
    dtype=torch.bfloat16,
    local_files_only=OFFLINE,
)

# Language detection model
audio_detection_model = whisper.load_model(
    "base",
)

# Text generation model
qwen2_5_model_path = _resolve_local_hf_snapshot("Qwen/Qwen2.5-1.5B-Instruct")
text_gen_tokenizer = AutoTokenizer.from_pretrained(
    qwen2_5_model_path or "Qwen/Qwen2.5-1.5B-Instruct",
    local_files_only=OFFLINE,
)
text_gen_model = AutoModelForCausalLM.from_pretrained(
    qwen2_5_model_path or "Qwen/Qwen2.5-1.5B-Instruct",
    device_map="auto",
    dtype="auto",
    local_files_only=OFFLINE,
)