from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..base import BaseFeatureModel, grammar_example_sentence_link, grammar_example_word_link

class Grammar(BaseFeatureModel):
    __tablename__ = 'grammar'
    __mapper_args__ = {"polymorphic_identity": "grammar"}
    
    title = Column(String, index=True)
    explanation = Column(String)
    
    # Relations
    example_words = relationship(                 # 1 to Many
        'Word',
        secondary=grammar_example_word_link,
        back_populates='grammar'
    )
    example_sentences = relationship(                 # 1 to Many
        'Passage',
        secondary=grammar_example_sentence_link,
        back_populates='grammar'
    )
    
    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict = {
            **super().to_dict(include_relations=include_relations),
            "title": self.title,
            "explanation": self.explanation
        }
        if include_relations:
            base_dict.update({
                "example_words": [word.to_dict(include_relations=False) for word in self.example_words],
                "example_sentences": [sentence.to_dict(include_relations=False) for sentence in self.example_sentences]
            })
        return base_dict