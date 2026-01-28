import re
from sqlalchemy import Column, String, Integer, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date

from ..core.database import Base
from .unit import Unit
from .language import Language
from .exercise import Exercise
from .associations import exercise_grammar_association

class Grammar(Base):
    __tablename__ = 'grammar'
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    explanation = Column(String)
    learnable_sentence = Column(String, default="")
    score = Column(Integer, default=0)
    last_seen = Column(Date, default=date.today)  # e.g., when the grammar rule was last seen

    parent_unit: Mapped["Unit"] = relationship("Unit", back_populates="grammars")
    unit_id: Mapped[str] = mapped_column(ForeignKey("unit.id"))

    parent_language: Mapped["Language"] = relationship("Language", back_populates="grammars")
    language_id: Mapped[str] = mapped_column(ForeignKey("language.id"))

    associated_exercises: Mapped[list["Exercise"]] = relationship(
        "Exercise",
        secondary=exercise_grammar_association,
        back_populates="associated_grammars"
    )

    exercise_ids: Mapped[list[str]] = mapped_column(JSON, default=list)

    def to_dict(self):
        return 
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "explanation": self.explanation,
            "learnable_sentence": self.learnable_sentence,
            "score": self.score,
            "last_seen": self.last_seen.isoformat(),
            "unit_id": self.unit_id,
            "language_id": self.language_id,
            "exercise_ids": self.exercise_ids,
        }