from typing import Optional

from ..base import BaseDataCollectionDict

class CommitmentLogDict(BaseDataCollectionDict):

    week_start_date: Optional[str] = None  # ISO date string (YYYY-MM-DD)
    days_active: int = 0
    total_items_reviewed: int = 0
    total_time_ms: int = 0
    weekly_goal_met: bool = False
    longest_streak_ever: int = 0
    streak_last_computed_at: str = ""  # ISO datetime string