from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..base import BaseFeatureModel

class Vocabulary(BaseFeatureModel):
    __tablename__ = 'vocabulary'
    
    # Foreign key
    word_id = Column(Integer, ForeignKey('word.id'), nullable=False)
    
    # Relationships
    word = relationship('Word', back_populates='vocabulary')    # Many to One
    example_sentences = relationship(                           # One to Many
        'Passage',
        back_populates='vocabulary',
        cascade='all, delete-orphan'
    )

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(include_relations=include_relations),
            "word": self.word.to_dict(include_relations=False),
            "example_sentences": [sentence.to_dict(include_relations=False) for sentence in self.example_sentences],
        }
        return base_dict