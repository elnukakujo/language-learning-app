from typing import Optional, List

from ..base import BaseFeatureDict
from ..components import PassageDict

class GrammarDict(BaseFeatureDict):
    title: str
    explanation: str
    learnable_sentences: Optional[List[PassageDict]] = None