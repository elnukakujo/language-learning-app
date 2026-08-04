import os
import urllib.request


def is_offline() -> bool:
    try:
        urllib.request.urlopen("https://huggingface.co", timeout=3)
        return False
    except Exception:
        return True


def configure_offline_environment() -> bool:
    offline = is_offline()
    if offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
    return offline