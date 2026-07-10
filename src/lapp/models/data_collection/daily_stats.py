from sqlalchemy import Column, Integer, Boolean, Float

from ..base import BaseDataCollectionModel

class DailyStats(BaseDataCollectionModel):
    __tablename__ = 'daily_stats'

    items_reviewed = Column(Integer, nullable=False)
    items_correct = Column(Integer, nullable=False)
    time_studied_ms = Column(Float, nullable=False)
    streak_day = Column(Boolean, nullable=False, default=False)
    current_streak_length = Column(Integer, nullable=False)

    def to_dict(self, include_relations: bool = False) -> dict:
        return {
            **super().to_dict(),
            "items_reviewed": self.items_reviewed,
            "items_correct": self.items_correct,
            "time_studied_ms": self.time_studied_ms,
            "streak_day": self.streak_day,
            "current_streak_length": self.current_streak_length,
        }