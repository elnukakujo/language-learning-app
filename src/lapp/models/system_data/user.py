from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime

from ...core.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    last_review = Column(DateTime, nullable=False, default=datetime.now())

    def to_dict(self, include_relations: bool = True) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_review": self.last_review.isoformat() if self.last_review else None
        }