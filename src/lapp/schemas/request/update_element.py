from typing import Any

from .base import BaseRequest

class UpdateElementRequest(BaseRequest):
    element_id: str
    updates: dict[str, Any]  # e.g. {"word": "new_word", "translation": "new_translation"}