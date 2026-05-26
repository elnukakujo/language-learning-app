from ..base import BaseDataCollectionDict

class CommitmentLogDict(BaseDataCollectionDict):

    days_active: int = 0
    total_items_reviewed: int = 0
    total_time_ms: int = 0
    longest_streak_ever: int = 0
    streak_last_computed_at: str = ""  # ISO datetime string