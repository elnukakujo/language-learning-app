from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import pandas as pd

engine = create_engine('sqlite:///vocab.db')

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Unit(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    objectives = Column(String, nullable=True)
    level = Column(String, nullable=False)

    def __repr__(self):
        return f"<Unit(title='{self.title}', level='{self.level}')>"

class ChineseUnit(Unit):
    __tablename__ = 'chinese_units'

    # One unit has many ChineseVocabulary entries
    vocab = relationship("ChineseVocabulary", back_populates="unit", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ChineseUnit(title='{self.title}', level='{self.level}')>"

class Vocabulary(Base):    
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False, unique=True)
    translation = Column(String, nullable=False, unique=True)
    type = Column(String, nullable=True)
    level = Column(String, nullable=False)

    def __repr__(self):
        return f"<Vocabulary(word='{self.word}', definition='{self.translation}, type='{self.type}', level='{self.level}')>"
    
class ChineseVocabulary(Vocabulary):
    __tablename__ = 'chinese_vocabulary'

    pinyin = Column(String, nullable=False, unique=False)
    unit_id = Column(Integer, ForeignKey('chinese_units.id'), nullable=False)

    # One vocabulary word belongs to one ChineseUnit
    unit = relationship("ChineseUnit", back_populates="vocab")

    def __repr__(self):
        return f"<ChineseVocabulary(word='{self.word}', pinyin='{self.pinyin}', translation='{self.translation}', type='{self.type}', level='{self.level}')>"

Base.metadata.create_all(engine)

if __name__ == "__main__":
    unit = ChineseUnit(
        title="Unite 15: A la maison",
        description='',
        objectives="A l'oral: Decrire une maison, un appartement\nUtiliser 吧 et les directionnels\nA l'ecrit: 17 caracteres",
        level='A2'
    )

    words = []

    for _, row in pd.read_csv('vocabulary_csv/unit15.csv').iterrows():
        words.append(ChineseVocabulary(
            word=row["word"],
            pinyin=row["pinyin"],
            translation=row["translation"],
            type=row["type"],
            level=unit.level,
            unit=unit
        ))

    session.add_all(words)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")
    
    for unit in session.query(ChineseUnit).all():
        print(unit.__repr__())

    session.close()