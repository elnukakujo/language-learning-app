from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .dbms import Base
from datetime import date

class Language(Base):
    __tablename__ = 'language'

    language_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    native_name = Column(String)
    level = Column(String)
    description = Column(String, default="")
    score = Column(Integer, default=0)
    last_seen = Column(Date, default=date.today)
    flag = Column(String, default="")

    # Foreign key to current unit
    current_unit = Column(String, ForeignKey("unit.unit_id"), nullable=True)

    # One-to-many: all units belonging to this language
    units: Mapped[list["Unit"]] = relationship(
        "Unit",
        back_populates="parent",
        cascade="all, delete-orphan",
        foreign_keys="[Unit.language_id]"  # ← Disambiguate here
    )

    # One-to-one: current unit relationship (optional, but useful)
    current_unit_obj: Mapped["Unit"] = relationship(
        "Unit",
        foreign_keys=[current_unit],
        uselist=False
    )

class Unit(Base):
    __tablename__ = 'unit'

    unit_id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    level = Column(String)
    score = Column(Integer, default=0)

    language_id: Mapped[str] = mapped_column(ForeignKey("language.language_id"))

    # Many-to-one: parent language
    parent: Mapped["Language"] = relationship(
        "Language",
        back_populates="units",
        foreign_keys=[language_id]
    )

    characters: Mapped[list["CalligraphyCharacter"]] = relationship(back_populates="parent", cascade="all, delete-orphan")
    grammars: Mapped[list["GrammarRule"]] = relationship(back_populates="parent", cascade="all, delete-orphan")
    vocs: Mapped[list["Vocabulary"]] = relationship(back_populates="parent", cascade="all, delete-orphan")
    exercises: Mapped[list["Exercise"]] = relationship(back_populates="parent", cascade="all, delete-orphan")

class CalligraphyCharacter(Base):
    __tablename__ = 'calligraphy_character'

    learn_id = Column(String, primary_key=True, index=True)
    character = Column(String, index=True)
    translation = Column(String)
    components = Column(String)
    score = Column(Integer, default=0)  # e.g., how much the character is mastered
    last_seen = Column(Date, default=date.today)  # e.g., when the character was last seen

    parent: Mapped["Unit"] = relationship("Unit", back_populates="characters")
    unit_id: Mapped[int] = mapped_column(ForeignKey("unit.unit_id"))


class GrammarRule(Base):
    __tablename__ = 'grammar_rule'
    
    learn_id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    explanation = Column(String)
    score = Column(Integer, default=0)
    last_seen = Column(Date, default=date.today)  # e.g., when the grammar rule was last seen

    parent: Mapped["Unit"] = relationship("Unit", back_populates="grammars")
    unit_id: Mapped[int] = mapped_column(ForeignKey("unit.unit_id"))

class Vocabulary(Base):
    __tablename__ = 'vocabulary'
    
    learn_id = Column(String, primary_key=True, index=True)
    word = Column(String, index=True)
    translation = Column(String)
    phonetic = Column(String)
    example_sentence = Column(String)
    type = Column(String)  # e.g., noun, verb, adjective
    score = Column(Integer, default=0)  # e.g., how much the vocabulary is mastered
    last_seen = Column(Date, default=date.today)  # e.g., when the vocabulary was last seen

    parent: Mapped["Unit"] = relationship("Unit", back_populates="vocs")
    unit_id: Mapped[int] = mapped_column(ForeignKey("unit.unit_id"))

class Exercise(Base):
    __tablename__ = 'exercises'

    learn_id = Column(String, primary_key=True, index=True)
    exercise_type = Column(String, index=True)  # e.g., multiple choice, fill
    question = Column(String, index=True)
    support = Column(String)  # e.g., image, audio, text
    answer = Column(String)
    score = Column(Integer, default=0)  # e.g., how much the exercise has been practiced
    last_seen = Column(Date, default=date.today)  # e.g., when the exercise was last seen

    parent: Mapped["Unit"] = relationship("Unit", back_populates="exercises")
    unit_id: Mapped[int] = mapped_column(ForeignKey("unit.unit_id"))