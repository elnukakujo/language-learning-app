from typing import Optional

from ..base import BaseDataCollectionDict

class DailyStatsDict(BaseDataCollectionDict):
    items_reviewed: Optional[int] = None
    items_correct: Optional[int] = None
    time_studied_ms: Optional[int] = None
    streak_day: Optional[bool] = None
    current_streak_length: Optional[int] = None