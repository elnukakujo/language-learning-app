import os
import socket


def is_offline() -> bool:
    try:
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return False
    except OSError:
        return True


def configure_offline_environment() -> bool:
    offline = is_offline()
    if offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
    return offline