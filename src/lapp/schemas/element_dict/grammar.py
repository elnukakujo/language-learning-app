from typing import Optional

from .base import BaseComponentDict

class GrammarDict(BaseComponentDict):
    title: str
    explanation: str
    learnable_sentence: Optional[str] = None