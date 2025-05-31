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

to_delete = input("Enter the string to search: ")

if input("Word? (y/n): ").lower() == 'y':
    # Find the record
    record = session.query(ChineseVocabulary).filter_by(word=to_delete).first()
elif input("Translation? (y/n): ").lower() == 'y':
    record = session.query(ChineseVocabulary).filter_by(translation=to_delete).first()

# If it exists, delete it
if record:
    input = input(f"Existing record found: {record}. Do you want to delete it? (y/n): ")
    if input.lower() != 'y':
        print("Deletion cancelled.")
    else:
        session.delete(record)
        session.commit()
        print(f"Deleted: {record}")
else:
    print(f"No record found with word '{to_delete}'")
