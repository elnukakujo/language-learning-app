from datetime import datetime
from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from ...core.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    display_name = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True)
    password_hash = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    last_review = Column(DateTime, nullable=False, default=datetime.now)

    # One-to-one relationship with UserPreferences
    preferences = relationship("UserPreferences", back_populates="user", uselist=False)

    def to_dict(self, include_relations: bool = True) -> dict:
        base = {
            "id": self.id,
            "username": self.username,
            "display_name": self.display_name,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_review": self.last_review.isoformat() if self.last_review else None
        }
        if include_relations and self.preferences:
            base["preferences"] = self.preferences.to_dict(include_relations=False)
        return base