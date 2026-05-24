from typing import Optional

from ..base import BaseComponentDict

class PassageDict(BaseComponentDict):
    text: str
    translation: Optional[str] = None

    characters: Optional[list[dict]] = None  # List of character
    words: Optional[list[dict]] = None  # List of word