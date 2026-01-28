from sqlalchemy import Column, String, Integer, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date

from ..core.database import Base
from .language import Language
from .unit import Unit
from .exercise import Exercise
from .associations import exercise_vocabulary_association

class Vocabulary(Base):
    __tablename__ = 'vocabulary'
    
    id = Column(String, primary_key=True, index=True)
    word = Column(String, index=True)
    translation = Column(String)
    phonetic = Column(String, default="")
    example_sentence = Column(String, default="")
    type = Column(String, default="")  # e.g., noun, verb, adjective
    score = Column(Integer, default=0)  # e.g., how much the vocabulary is mastered
    last_seen = Column(Date, default=date.today)  # e.g., when the vocabulary was last seen

    parent_unit: Mapped["Unit"] = relationship("Unit", back_populates="vocabularies")
    unit_id: Mapped[str] = mapped_column(ForeignKey("unit.id")) 

    parent_language: Mapped["Language"] = relationship("Language", back_populates="vocabularies")
    language_id: Mapped[str] = mapped_column(ForeignKey("language.id"))

    associated_exercises: Mapped[list["Exercise"]] = relationship(
        "Exercise",
        secondary=exercise_vocabulary_association,
        back_populates="associated_vocabularies"
    )

    exercise_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "word": self.word,
            "translation": self.translation,
            "phonetic": self.phonetic,
            "example_sentence": self.example_sentence,
            "type": self.type,
            "score": self.score,
            "last_seen": self.last_seen.isoformat(),
            "unit_id": self.unit_id,
            "language_id": self.language_id,
            "exercise_ids": self.exercise_ids,
        }