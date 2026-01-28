from sqlalchemy import Column, Integer, String, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date

from ..core.database import Base
from .unit import Unit
from .language import Language
from .associations import (
    exercise_vocabulary_association,
    exercise_character_association,
    exercise_grammar_association
)

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

    parent_unit: Mapped["Unit"] = relationship("Unit", back_populates="exercises")
    unit_id: Mapped[str] = mapped_column(ForeignKey("unit.id")) 

    parent_language: Mapped["Language"] = relationship("Language", back_populates="exercises")
    language_id: Mapped[str] = mapped_column(ForeignKey("language.id"))

    # Relationships to learning components
    associated_vocabularies: Mapped[list["Vocabulary"]] = relationship(
        "Vocabulary",
        secondary=exercise_vocabulary_association,
        back_populates="associated_exercises"
    )
    associated_characters: Mapped[list["Character"]] = relationship(
        "Character",
        secondary=exercise_character_association,
        back_populates="associated_exercises"
    )
    associated_grammars: Mapped[list["Grammar"]] = relationship(
        "Grammar",
        secondary=exercise_grammar_association,
        back_populates="associated_exercises"
    )

    character_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    grammar_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    vocabulary_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    
    def to_dict(self) -> dict:
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
            "unit_id": self.unit_id,
            "language_id": self.language_id,
            "character_ids": self.character_ids,
            "grammar_ids": self.grammar_ids,
            "vocabulary_ids": self.vocabulary_ids,
        }