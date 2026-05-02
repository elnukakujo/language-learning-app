from typing import Optional, List

from ..base import BaseFeatureDict
from ..components import CharacterDict, WordDict, PassageDict

class CalligraphyDict(BaseFeatureDict):
    character: CharacterDict
    example_words: Optional[List[WordDict]] = None  # Example word using the character
    example_sentences: Optional[List[PassageDict]] = None  # Example sentence using the character