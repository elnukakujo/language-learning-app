from sqlalchemy import Column, String, Integer, Date, ForeignKey
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

    # Many-to-one: parent language
    parent_language: Mapped["Language"] = relationship("Language",back_populates="units")
    language_id: Mapped[str] = mapped_column(ForeignKey("language.id"))

    # One-to-many: all related models
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

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "level": self.level,
            "score": self.score,
            "last_seen": self.last_seen.isoformat(),
            "language_id": self.language_id
        }