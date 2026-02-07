from typing import Optional

from ..base import BaseComponentDict

class CharacterDict(BaseComponentDict):
    character: str
    phonetic: str
    meaning: Optional[str] = None
    radical: Optional[str] = None
    strokes: Optional[int] = None