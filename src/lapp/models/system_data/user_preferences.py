from datetime import datetime
from sqlalchemy import Column, String, Date, JSON, ForeignKey

from ...core.database import Base


class UserPreferences(Base):
    __tablename__ = 'user_preferences'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('user.id'), nullable=False, unique=True)
    native_language_iso639_2 = Column(JSON, nullable=False, default=list)
    learning_goals = Column(String, default='')
    preferred_exercise_types = Column(JSON, default=list)
    last_updated = Column(Date, default=datetime.now())

