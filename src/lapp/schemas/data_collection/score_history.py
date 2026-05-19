from typing import Optional

from ..base import BaseDataCollectionDict, BaseElementDict

class ScoreHistoryDict(BaseDataCollectionDict):
    element_type: Optional[str] = None
    score_before: Optional[float] = None
    score_after: Optional[float] = None

    element: Optional[BaseElementDict] = None