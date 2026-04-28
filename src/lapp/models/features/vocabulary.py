from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from ..base import BaseFeatureModel, vocabulary_example_sentence_link

class Vocabulary(BaseFeatureModel):
    __tablename__ = 'vocabulary'
    
    # Foreign key
    word_id = Column(String, ForeignKey('word.id'), nullable=False)
    
    # Relationships
    word = relationship('Word', back_populates='vocabulary')    # Many to One
    example_sentences = relationship(                           # One to Many
        'Passage',
        secondary=vocabulary_example_sentence_link,
        back_populates='vocabulary'
    )

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(include_relations=include_relations),
            "word": self.word.to_dict(include_relations=False),
            "example_sentences": [sentence.to_dict(include_relations=False) for sentence in self.example_sentences],
            "word_id": self.word_id,
        }
        return base_dict