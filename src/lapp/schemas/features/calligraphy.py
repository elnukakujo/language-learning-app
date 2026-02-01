from typing import Optional

from ..base import BaseFeatureDict
from ..components import CharacterDict, WordDict

class CalligraphyDict(BaseFeatureDict):
    character: CharacterDict
    example_word: Optional[WordDict] = None  # Example word using the character