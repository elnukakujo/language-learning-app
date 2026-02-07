from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..base import BaseContainerModel

class Unit(BaseContainerModel):
    __tablename__ = 'unit'

    title = Column(String, index=True)
    description = Column(String)
    level = Column(String)

    # Foreign key
    language_id: Mapped[str] = mapped_column(ForeignKey('language.id'))

    # Relationships
    language: Mapped["Language"] = relationship(
        "Language",
        back_populates="unit",
    )
    calligraphy: Mapped[list["Calligraphy"]] = relationship(
        "Calligraphy",
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
                "calligraphy_ids": [calligraphy.id for calligraphy in self.calligraphy],
                "grammar_ids": [grammar.id for grammar in self.grammar],
                "vocabulary_ids": [vocab.id for vocab in self.vocabulary],
                "exercise_ids": [ex.id for ex in self.exercise]
            })
        return base_dict