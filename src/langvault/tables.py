from sqlalchemy import Column, Integer, String, ForeignKey
from .dbms import Base

class Unit(Base):
    __tablename__ = 'units'
    
    unit_id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    level = Column(String)
    
class CalligraphyCharacter(Base):
    __tablename__ = 'calligraphy_characters'

    char_id = Column(String, primary_key=True, index=True)
    unit_id = Column(String, ForeignKey('units.unit_id'), index=True)
    character = Column(String, index=True)
    char_translation = Column(String)
    components = Column(String)

class GrammarRule(Base):
    __tablename__ = 'grammar_rules'
    
    grammar_id = Column(String, primary_key=True, index=True)
    unit_id = Column(String, ForeignKey('units.unit_id'), index=True)
    grammar_title = Column(String, index=True)
    explanation = Column(String)

class Vocabulary(Base):
    __tablename__ = 'vocabulary'
    
    voc_id = Column(String, primary_key=True, index=True)
    unit_id = Column(String, ForeignKey('units.unit_id'), index=True)
    word = Column(String, index=True)
    voc_translation = Column(String)
    voc_phonetic = Column(String)
    example_sentence = Column(String)
    voc_type = Column(String)  # e.g., noun, verb, adjective

class Exercise(Base):
    __tablename__ = 'exercises'

    exercise_id = Column(String, primary_key=True, index=True)
    unit_id = Column(String, ForeignKey('units.unit_id'), index=True)
    exercise_type = Column(String, index=True)  # e.g., multiple choice, fill
    question = Column(String, index=True)
    support = Column(String)  # e.g., image, audio, text
    answer = Column(String)