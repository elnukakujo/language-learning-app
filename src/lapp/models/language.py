from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Mapped

from .base import BaseModel
from .unit import Unit

class Language(BaseModel):
    __tablename__ = 'language'

    name = Column(String, index=True)
    native_name = Column(String)
    level = Column(String)
    description = Column(String, default="")
    flag = Column(String, default="")

    # Foreign key to current unit
    current_unit = Column(String, nullable=True)

    # One-to-many: all units belonging to this language
    unit: Mapped[list["Unit"]] = relationship(
        "Unit",
        back_populates="language",
        cascade="all, delete-orphan",
    )

    # One-to-many: all characters/grammars/vocabularies/exercises belonging to this language
    character: Mapped[list["Character"]] = relationship(
        "Character",
        back_populates="language",
        cascade="all, delete-orphan"
    )
    grammar: Mapped[list["Grammar"]] = relationship(
        "Grammar",
        back_populates="language",
        cascade="all, delete-orphan"
    )
    vocabulary: Mapped[list["Vocabulary"]] = relationship(
        "Vocabulary",
        back_populates="language",
        cascade="all, delete-orphan"
    )
    exercise: Mapped[list["Exercise"]] = relationship(
        "Exercise",
        back_populates="language",
        cascade="all, delete-orphan"
    )

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(),
            "name": self.name,
            "native_name": self.native_name,
            "level": self.level,
            "description": self.description,
            "flag": self.flag,
            "current_unit": self.current_unit
        }

        if include_relations:
            base_dict.update({
                "unit_ids": [unit.id for unit in self.unit],
                "character_ids": [char.id for char in self.character],
                "grammar_ids": [gram.id for gram in self.grammar],
                "vocabulary_ids": [vocab.id for vocab in self.vocabulary],
                "exercise_ids": [ex.id for ex in self.exercise],
            })
        
        return base_dict