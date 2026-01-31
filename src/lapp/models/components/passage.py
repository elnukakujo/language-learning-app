from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from ..base import BaseComponentModel

class Passage(BaseComponentModel):
    __tablename__ = 'passage'
    
    text = Column(Text, nullable=False)
    translation = Column(Text, nullable=False)
    
    # Foreign key
    vocabulary_id = Column(Integer, ForeignKey('vocabulary.id'), nullable=True)
    grammar_id = Column(Integer, ForeignKey('grammar.id'), nullable=True)

    # Relationship
    vocabulary = relationship('Vocabulary', back_populates='example_sentences')      # Many to One
    grammar = relationship('Grammar', back_populates='learnable_sentences')          # Many to One

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(),
            "text": self.text,
            "translation": self.translation
        }
        if include_relations:
            base_dict.update({
                "vocabulary_id": self.vocabulary_id,
                "grammar_id": self.grammar_id
            })
        return base_dict