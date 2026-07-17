from datetime import date
from sqlalchemy import Column, Integer, String, Date, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from ...core.database import Base


class UserPreferences(Base):
    __tablename__ = 'user_preferences'

    id = Column(String, primary_key=True, index=True)
    native_language_iso639_2 = Column(JSON, nullable=False, default=lambda: ["eng"])
    learning_goals = Column(String, default='')
    preferred_exercise_types = Column(JSON, default=list)
    daily_goal_minutes = Column(Integer, default=20, nullable=False)
    last_updated = Column(Date, default=date.today)
    ai_feedback_enabled = Column(Boolean, default=True, nullable=False)
    ai_text_gen_enabled = Column(Boolean, default=True, nullable=False)
    ai_tts_enabled = Column(Boolean, default=True, nullable=False)
    
    # Foreign keys
    user_id = Column(String, ForeignKey('user.id'), nullable=False, unique=True)

    # Relationship back to User
    user = relationship(
        "User",
        back_populates="preferences",
        foreign_keys="[UserPreferences.user_id]"
    )
    
    def to_dict(self, include_relations: bool = True) -> dict:
        base = {
            "id": self.id,
            "user_id": self.user_id,
            "native_language_iso639_2": self.native_language_iso639_2,
            "learning_goals": self.learning_goals,
            "preferred_exercise_types": self.preferred_exercise_types,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "ai_feedback_enabled": self.ai_feedback_enabled,
            "ai_text_gen_enabled": self.ai_text_gen_enabled,
            "ai_tts_enabled": self.ai_tts_enabled,
        }
        if include_relations and self.user:
            base["user"] = self.user.to_dict(include_relations=False)
        return base