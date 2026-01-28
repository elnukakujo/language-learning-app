from sqlalchemy import Column, String, Integer, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date

from ..core.database import Base

class Unit(Base):
    __tablename__ = 'unit'

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    level = Column(String)
    score = Column(Integer, default=0)
    last_seen = Column(Date, default=date.today)

    # Relationships
    parent_language: Mapped["Language"] = relationship(
        "Language",
        back_populates="units"
    )

    characters: Mapped[list["Character"]] = relationship(
        "Character",
        back_populates="parent_unit",
        cascade="all, delete-orphan"
    )
    grammars: Mapped[list["Grammar"]] = relationship(
        "Grammar",
        back_populates="parent_unit",
        cascade="all, delete-orphan"
    )
    vocabularies: Mapped[list["Vocabulary"]] = relationship(
        "Vocabulary",
        back_populates="parent_unit",
        cascade="all, delete-orphan"
    )
    exercises: Mapped[list["Exercise"]] = relationship(
        "Exercise",
        back_populates="parent_unit",
        cascade="all, delete-orphan"
    )
    
    # Save IDs of related models for quick access
    language_id: Mapped[str] = mapped_column(ForeignKey("language.id"))

    character_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    grammar_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    vocabulary_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    exercise_ids: Mapped[list[str]] = mapped_column(JSON, default=list)

    def to_dict(self) -> dict:
        print(self.id)
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "level": self.level,
            "score": self.score,
            "last_seen": self.last_seen.isoformat(),
            "language_id": self.language_id,
            "character_ids": self.character_ids,
            "grammar_ids": self.grammar_ids,
            "vocabulary_ids": self.vocabulary_ids,
            "exercise_ids": self.exercise_ids,
        }