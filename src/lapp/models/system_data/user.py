from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime

from ...core.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    last_review = Column(DateTime, nullable=False, default=datetime.now)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    def to_dict(self, include_relations: bool = True) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "last_review": self.last_review.isoformat(),
            "created_at": self.created_at.isoformat(),
        }