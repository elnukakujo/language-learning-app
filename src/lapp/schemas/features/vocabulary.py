from typing import Optional, List

from ..base import BaseFeatureDict
from ..components import WordDict, PassageDict

class VocabularyDict(BaseFeatureDict):
    word: WordDict
    example_sentences: Optional[List[PassageDict]] = None  # Example sentence using the word