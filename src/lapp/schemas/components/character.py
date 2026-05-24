from typing import Optional

from ..base import BaseComponentDict

class CharacterDict(BaseComponentDict):
    character: str
    phonetic: Optional[str] = None
    meaning: Optional[str] = None
    radical: Optional[str] = None
    strokes: Optional[int] = None

    words: Optional[list[dict]] = None  # List of word
    passages: Optional[list[dict]] = None  # List of passage