from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date

from ..core.database import Base
from .unit import Unit
from .language import Language
from .exercise import Exercise
from .associations import exercise_character_association

class Character(Base):
    __tablename__ = 'character'

    id = Column(String, primary_key=True, index=True)
    character = Column(String, index=True)  # e.g., the character itself
    components = Column(String, default="")
    phonetic = Column(String)  # e.g., pinyin for Chinese characters
    meaning = Column(String)
    example_word = Column(String, default="")
    score = Column(Integer, default=0)  # e.g., how much the character is mastered
    last_seen = Column(Date, default=date.today)  # e.g., when the character was last seen

    parent_unit: Mapped["Unit"] = relationship("Unit", back_populates="characters")
    unit_id: Mapped[str] = mapped_column(ForeignKey("unit.id"))

    parent_language: Mapped["Language"] = relationship("Language", back_populates="characters")
    language_id: Mapped[str] = mapped_column(ForeignKey("language.id"))

    associated_exercises: Mapped[list["Exercise"]] = relationship(
        "Exercise",
        secondary=exercise_character_association,
        back_populates="associated_char"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "character": self.character,
            "components": self.components,
            "phonetic": self.phonetic,
            "meaning": self.meaning,
            "example_word": self.example_word,
            "score": self.score,
            "last_seen": self.last_seen.isoformat(),
            "unit_id": self.unit_id,
            "language_id": self.language_id
        }