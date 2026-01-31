from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..base import BaseComponentModel

class Word(BaseComponentModel):
    __tablename__ = 'word'
    
    word = Column(String(255), nullable=False, index=True, unique=True)
    translation = Column(String(500), nullable=False)
    phonetic = Column(String(255), nullable=True)
    type = Column(String(100), nullable=True)  # e.g., noun, verb, adjective
    
    # Relationship
    vocabulary = relationship('Vocabulary', back_populates='word')      # 1 to Many
    calligraphy = relationship('Calligraphy', back_populates='example_word')  # One to Many

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(),
            "word": self.word,
            "translation": self.translation,
            "phonetic": self.phonetic,
            "type": self.type
        }
        if include_relations:
            base_dict.update({
                "vocabulary_ids": [v.id for v in self.vocabulary],
                "calligraphy_ids": [cf.id for cf in self.calligraphy]
            })
        return base_dict