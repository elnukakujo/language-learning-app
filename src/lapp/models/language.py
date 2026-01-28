from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from datetime import date

from ..core.database import Base
from .unit import Unit

class Language(Base):
    __tablename__ = 'language'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    native_name = Column(String)
    level = Column(String)
    description = Column(String, default="")
    score = Column(Integer, default=0)
    last_seen = Column(Date, default=date.today)
    flag = Column(String, default="")

    # Foreign key to current unit
    current_unit = Column(String, ForeignKey("unit.id"), nullable=True)

    # One-to-many: all units belonging to this language
    units: Mapped[list["Unit"]] = relationship(
        "Unit",
        back_populates="parent_language",
        cascade="all, delete-orphan",
        foreign_keys=lambda: [Unit.language_id]
    )

    # One-to-many: all characters/grammars/vocabularies/exercises belonging to this language
    characters: Mapped[list["Character"]] = relationship(
        "Character",
        back_populates="parent_language",
        cascade="all, delete-orphan"
    )
    grammars: Mapped[list["Grammar"]] = relationship(
        "Grammar",
        back_populates="parent_language",
        cascade="all, delete-orphan"
    )
    vocabularies: Mapped[list["Vocabulary"]] = relationship(
        "Vocabulary",
        back_populates="parent_language",
        cascade="all, delete-orphan"
    )
    exercises: Mapped[list["Exercise"]] = relationship(
        "Exercise",
        back_populates="parent_language",
        cascade="all, delete-orphan"
    )

    def to_dict(self, include_relationships: bool = False) -> dict:
        base_dict = {
            "id": self.id,
            "name": self.name,
            "native_name": self.native_name,
            "level": self.level,
            "description": self.description,
            "flag": self.flag,
            "current_unit": self.current_unit,
            "score": self.score,
            "last_seen": self.last_seen.isoformat(),
        }
        if include_relationships:
            base_dict.update({
                "unit_ids": [unit.id for unit in self.units],
                "character_ids": [char.id for char in self.characters],
                "grammar_ids": [gram.id for gram in self.grammars],
                "vocabulary_ids": [vocab.id for vocab in self.vocabularies],
                "exercise_ids": [ex.id for ex in self.exercises],
            })
        return base_dict