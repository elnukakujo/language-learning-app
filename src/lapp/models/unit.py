from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date

from ..core.database import Base
from . import Character, Grammar, Vocabulary, Exercise, Language

class Unit(Base):
    __tablename__ = 'unit'

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    level = Column(String)
    score = Column(Integer, default=0)
    last_seen = Column(Date, default=date.today)
    
    language_id: Mapped[str] = mapped_column(ForeignKey("language.id"))

    # Many-to-one: parent language
    parent: Mapped["Language"] = relationship(
        "Language",
        back_populates="units",
        foreign_keys=[language_id]
    )

    characters: Mapped[list["Character"]] = relationship(back_populates="parent", cascade="all, delete-orphan")
    grammars: Mapped[list["Grammar"]] = relationship(back_populates="parent", cascade="all, delete-orphan")
    vocs: Mapped[list["Vocabulary"]] = relationship(back_populates="parent", cascade="all, delete-orphan")
    exercises: Mapped[list["Exercise"]] = relationship(back_populates="parent", cascade="all, delete-orphan")

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