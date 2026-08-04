from typing import Optional, List

from ..base import BaseFeatureDict
from ..components import PassageDict, WordDict

class GrammarDict(BaseFeatureDict):
    title: str
    explanation: str
    example_words: Optional[List[WordDict]] = None  # Example words illustrating the grammar point
    example_sentences: Optional[List[PassageDict]] = None