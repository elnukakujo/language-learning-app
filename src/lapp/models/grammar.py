from sqlalchemy import Column, String

from .base import BaseComponentModel

class Grammar(BaseComponentModel):
    __tablename__ = 'grammar'
    
    title = Column(String, index=True)
    explanation = Column(String)
    learnable_sentence = Column(String, default="")
    
    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict = {
            **super().to_dict(include_relations=include_relations),
            "title": self.title,
            "explanation": self.explanation,
            "learnable_sentence": self.learnable_sentence
        }
        return base_dict