from sqlalchemy import Column, Integer, String, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date

from ..core.database import Base
from .unit import Unit

class Exercise(Base):
    __tablename__ = 'exercises'

    id = Column(String, primary_key=True, index=True)
    exercise_type = Column(String, index=True)  # e.g., multiple choice, fill
    question = Column(String, index=True)

    text_support = Column(String, default="")   # e.g., additional text information
    image_files = Column(JSON, default=list)    # e.g. list of image file paths
    audio_files = Column(JSON, default=list)    # e.g. list of audio file paths

    answer = Column(String)
    score = Column(Integer, default=0)  # e.g., how much the exercise has been practiced
    last_seen = Column(Date, default=date.today)  # e.g., when the exercise was last seen
    associated_to = Column(JSON, default={})

    parent: Mapped["Unit"] = relationship("Unit", back_populates="exercises")
    unit_id: Mapped[str] = mapped_column(ForeignKey("unit.id"))  # Fixed: should be str, not int

    def to_dict(self):
        return {
            "id": self.id,
            "exercise_type": self.exercise_type,
            "question": self.question,
            "text_support": self.text_support,
            "image_files": self.image_files,
            "audio_files": self.audio_files,
            "answer": self.answer,
            "score": self.score,
            "last_seen": self.last_seen.isoformat(),
            "associated_to": self.associated_to,
            "unit_id": self.unit_id
        }