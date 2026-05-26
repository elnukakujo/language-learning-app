from sqlalchemy import Column, Integer, Boolean, String

from ..base import BaseDataCollectionModel

class CommitmentLog(BaseDataCollectionModel):
    __tablename__ = 'commitment_log'

    days_active = Column(Integer, nullable=False)
    total_items_reviewed = Column(Integer, nullable=False)
    total_time_ms = Column(Integer, nullable=False)
    longest_streak_ever = Column(Integer, nullable=False)
    streak_last_computed_at = Column(String, nullable=False)  # ISO datetime string

    def to_dict(self, include_relations: bool = False) -> dict:
        return {
            **super().to_dict(),
            "days_active": self.days_active,
            "total_items_reviewed": self.total_items_reviewed,
            "total_time_ms": self.total_time_ms,
            "longest_streak_ever": self.longest_streak_ever,
            "streak_last_computed_at": self.streak_last_computed_at,
        }