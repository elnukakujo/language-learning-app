from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .dbms import Base
from datetime import date

class Unit(Base):
    __tablename__ = 'unit'
    
    unit_id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    level = Column(String)

    characters: Mapped[list["CalligraphyCharacter"]] = relationship(back_populates="parent", cascade="all, delete-orphan")
    grammars: Mapped[list["GrammarRule"]] = relationship(back_populates="parent", cascade="all, delete-orphan")
    vocs: Mapped[list["Vocabulary"]] = relationship(back_populates="parent", cascade="all, delete-orphan")
    exercises: Mapped[list["Exercise"]] = relationship(back_populates="parent", cascade="all, delete-orphan")

class CalligraphyCharacter(Base):
    __tablename__ = 'calligraphy_character'

    char_id = Column(String, primary_key=True, index=True)
    character = Column(String, index=True)
    char_translation = Column(String)
    components = Column(String)
    score = Column(Integer, default=0)  # e.g., how much the character is mastered
    last_seen = Column(Date, default=date.today)  # e.g., when the character was last seen

    parent: Mapped["Unit"] = relationship("Unit", back_populates="characters")
    unit_id: Mapped[int] = mapped_column(ForeignKey("unit.unit_id"))


class GrammarRule(Base):
    __tablename__ = 'grammar_rule'
    
    grammar_id = Column(String, primary_key=True, index=True)
    grammar_title = Column(String, index=True)
    explanation = Column(String)
    score = Column(Integer, default=0)
    last_seen = Column(Date, default=date.today)  # e.g., when the grammar rule was last seen

    parent: Mapped["Unit"] = relationship("Unit", back_populates="grammars")
    unit_id: Mapped[int] = mapped_column(ForeignKey("unit.unit_id"))

class Vocabulary(Base):
    __tablename__ = 'vocabulary'
    
    voc_id = Column(String, primary_key=True, index=True)
    word = Column(String, index=True)
    voc_translation = Column(String)
    voc_phonetic = Column(String)
    example_sentence = Column(String)
    voc_type = Column(String)  # e.g., noun, verb, adjective
    score = Column(Integer, default=0)  # e.g., how much the vocabulary is mastered
    last_seen = Column(Date, default=date.today)  # e.g., when the vocabulary was last seen

    parent: Mapped["Unit"] = relationship("Unit", back_populates="vocs")
    unit_id: Mapped[int] = mapped_column(ForeignKey("unit.unit_id"))

class Exercise(Base):
    __tablename__ = 'exercises'

    exercise_id = Column(String, primary_key=True, index=True)
    exercise_type = Column(String, index=True)  # e.g., multiple choice, fill
    question = Column(String, index=True)
    support = Column(String)  # e.g., image, audio, text
    answer = Column(String)
    score = Column(Integer, default=0)  # e.g., how much the exercise has been practiced
    last_seen = Column(Date, default=date.today)  # e.g., when the exercise was last seen

    parent: Mapped["Unit"] = relationship("Unit", back_populates="exercises")
    unit_id: Mapped[int] = mapped_column(ForeignKey("unit.unit_id"))