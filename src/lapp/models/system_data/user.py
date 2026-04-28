from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime

from ...core.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    day_streak = Column(Integer, nullable=False, default=0)
    last_review = Column(DateTime, nullable=False, default=datetime.now)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

