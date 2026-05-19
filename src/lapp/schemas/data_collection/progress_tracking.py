from typing import Optional

from ..base import BaseDataCollectionDict, BaseElementDict

class ProgressTrackingDict(BaseDataCollectionDict):
    element_type: Optional[str] = None
    element_status: Optional[str] = None
    new_score_difference: Optional[int] = None
    result: Optional[bool] = None
    duration_ms: Optional[float] = None
    hint_used: Optional[bool] = None
    attempt_number: Optional[int] = None
    session_completed: Optional[bool] = None

    element: Optional[BaseElementDict] = None