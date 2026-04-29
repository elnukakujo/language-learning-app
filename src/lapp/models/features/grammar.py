from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..base import BaseFeatureModel, grammar_example_sentence_link, grammar_example_word_link

class Grammar(BaseFeatureModel):
    __tablename__ = 'grammar'
    
    title = Column(String, index=True)
    explanation = Column(String)
    
    # Relations
    example_sentences = relationship(                 # 1 to Many
        'Passage',
        secondary=grammar_example_sentence_link,
        back_populates='grammar'
    )
    example_words = relationship(                 # 1 to Many
        'Word',
        secondary=grammar_example_word_link,
        back_populates='grammar'
    )
    
    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict = {
            **super().to_dict(include_relations=include_relations),
            "title": self.title,
            "explanation": self.explanation,
            "example_sentences": [p.to_dict(include_relations=False) for p in self.example_sentences],
            "example_words": [w.to_dict(include_relations=False) for w in self.example_words]
        }
        return base_dict