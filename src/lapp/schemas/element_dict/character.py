from typing import Optional

from .base import BaseElementDict

class CharacterDict(BaseElementDict):
    unit_id: str
    character: str
    components: Optional[str] = None  # Components of the character
    phonetic: str
    meaning: str
    example_word: Optional[str] = None  # Example word using the character