from sqlalchemy import Table, Column, String, ForeignKey
from ..core.database import Base

# Association table for Exercise-Vocabulary many-to-many
exercise_vocabulary_association = Table(
    'exercise_vocabulary',
    Base.metadata,
    Column('exercise_id', String, ForeignKey('exercises.id'), primary_key=True),
    Column('vocabulary_id', String, ForeignKey('vocabulary.id'), primary_key=True)
)

exercise_character_association = Table(
    'exercise_character',
    Base.metadata,
    Column('exercise_id', String, ForeignKey('exercises.id'), primary_key=True),
    Column('character_id', String, ForeignKey('characters.id'), primary_key=True)
)

exercise_grammar_association = Table(
    'exercise_grammar',
    Base.metadata,
    Column('exercise_id', String, ForeignKey('exercises.id'), primary_key=True),
    Column('grammar_id', String, ForeignKey('grammar.id'), primary_key=True)
)