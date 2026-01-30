from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import BaseModel

class Unit(BaseModel):
    __tablename__ = 'unit'

    title = Column(String, index=True)
    description = Column(String)
    level = Column(String)

    language_id: Mapped[str] = mapped_column(ForeignKey('language.id'))

    # Relationships
    language: Mapped["Language"] = relationship(
        "Language",
        back_populates="unit",
    )

    character: Mapped[list["Character"]] = relationship(
        "Character",
        back_populates="unit",
        cascade="all, delete-orphan"
    )
    grammar: Mapped[list["Grammar"]] = relationship(
        "Grammar",
        back_populates="unit",
        cascade="all, delete-orphan"
    )
    vocabulary: Mapped[list["Vocabulary"]] = relationship(
        "Vocabulary",
        back_populates="unit",
        cascade="all, delete-orphan"
    )
    exercise: Mapped[list["Exercise"]] = relationship(
        "Exercise",
        back_populates="unit",
        cascade="all, delete-orphan"
    )

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(),
            "title": self.title,
            "description": self.description,
            "level": self.level,
            "language_id": self.language_id
        }

        if include_relations:
            base_dict.update({
                "character_ids": [character.id for character in self.character],
                "grammar_ids": [grammar.id for grammar in self.grammar],
                "vocabulary_ids": [vocab.id for vocab in self.vocabulary],
                "exercise_ids": [ex.id for ex in self.exercise]
            })
        return base_dict