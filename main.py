from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import pandas as pd
import json
import os

engine = create_engine('sqlite:///vocab.db')

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Unit(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    objectives = Column(Text, nullable=True)
    level = Column(String, nullable=False)

    def __repr__(self):
        return f"<Unit(title='{self.title}', level='{self.level}')>"

class ChineseUnit(Unit):
    __tablename__ = 'chinese_units'

    # One unit has many ChineseVocabulary entries
    vocab = relationship("ChineseVocabulary", back_populates="unit", cascade="all, delete-orphan")
    # One unit has many ChineseGrammarSheet entries
    grammar_sheets = relationship("ChineseGrammarSheet", back_populates="unit", cascade="all, delete-orphan")
    # One unit has many ChineseDialogue entries
    dialogues = relationship("ChineseDialogue", back_populates="unit", cascade="all, delete-orphan")

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

class GrammarSheet(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    content = Column(Text, nullable=False)
    level = Column(String, nullable=False)

    def __repr__(self):
        return f"<GrammarSheet(title='{self.title}', level='{self.level}')>"
    
class ChineseGrammarSheet(GrammarSheet):
    __tablename__ = 'chinese_grammar_sheets'

    unit_id = Column(Integer, ForeignKey('chinese_units.id'), nullable=False)
    # One grammar sheet belongs to one ChineseUnit
    unit = relationship("ChineseUnit", back_populates="grammar_sheets")

    def __repr__(self):
        return f"<ChineseGrammarSheet(title='{self.title}', level='{self.level}, unit_id='{self.unit_id}')>"
    
class Speech(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    speaker = Column(Integer, nullable=False)
    sentence = Column(Text, nullable=False)
    translation = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Speech(speaker='{self.speaker}', sentence='{self.sentence}', translation='{self.translation}')>"
    
class ChineseSpeech(Speech):
    __tablename__ = 'chinese_speech'

    pinyin = Column(Text, nullable=False, unique=False)
    dialogue_id = Column(Integer, ForeignKey('chinese_dialogue.id'), nullable=False)
    # One speech belongs to one Dialogue
    dialogue = relationship("ChineseDialogue", back_populates="entries")

    def __repr__(self):
        return f"<ChineseSpeech(speaker='{self.speaker}', sentence='{self.sentence}', translation='{self.translation}', pinyin='{self.pinyin}')>"

class Dialogue(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    unit_id = Column(Integer, ForeignKey('chinese_units.id'), nullable=False)
    entries = Column(String, nullable=False)

    def __repr__(self):
        return f"<Dialogue(title='{self.title}', entries='{self.entries}')>"
    
class ChineseDialogue(Dialogue):
    __tablename__ = 'chinese_dialogue'

    unit_id = Column(Integer, ForeignKey('chinese_units.id'), nullable=False)
    # One dialogue belongs to one ChineseUnit
    unit = relationship("ChineseUnit", back_populates="dialogues")

    # One speech belongs to one ChineseDialogue
    entries = relationship("ChineseSpeech", back_populates="dialogue", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ChineseDialogue(title='{self.title}', unit_id='{self.unit_id}', entries='{self.entries}')>"

Base.metadata.create_all(engine)

if __name__ == "__main__":
    with open('data/units.json', 'r', encoding='utf-8') as f:
        unitsdata = json.load(f)
    for idx in range(len(unitsdata)):
        unit = ChineseUnit(
            title=unitsdata[idx]['title'],
            description=unitsdata[idx].get('description', ''),
            objectives=unitsdata[idx].get('objectives', ''),
            level=unitsdata[idx]['level']
        )
        session.add(unit)

        words = []

        for _, row in pd.read_csv(f'data/vocabulary/unit{idx}.csv').iterrows():
            words.append(ChineseVocabulary(
                word=row["word"],
                pinyin=row["pinyin"],
                translation=row["translation"],
                type=row["type"],
                level=unit.level,
                unit=unit
            ))

        session.add_all(words)

        if os.path.exists(f'data/grammar/unit{idx}.json'):
            grammar_sheets = []
            with open(f'data/grammar/unit{idx}.json', 'r', encoding='utf-8') as f:
                grammar_data = json.load(f)
            for element in grammar_data:
                grammar_sheets.append(ChineseGrammarSheet(
                    title=element["title"],
                    content=element["content"],
                    level=unit.level,
                    unit=unit
                ))

            session.add_all(grammar_sheets)

        if os.path.exists(f'data/dialog/unit{idx}.json'):
            dialogues = []
            with open(f'data/dialog/unit{idx}.json', 'r', encoding='utf-8') as f:
                dialogue_data = json.load(f)
            for element in dialogue_data:
                dialogue = ChineseDialogue(
                    title=element["title"],
                    unit=unit,
                    entries=[]
                )
                for entry in element["entries"]:
                    dialogue.entries.append(ChineseSpeech(
                        speaker=entry["role"],
                        sentence=entry["content"]["sentence"],
                        translation=entry["content"]["translation"],
                        pinyin=entry["content"]["pinyin"],
                        dialogue=dialogue
                    ))
                dialogues.append(dialogue)

            session.add_all(dialogues)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")
    
    for unit in session.query(ChineseUnit).all():
        print(unit.__repr__())

    session.close()