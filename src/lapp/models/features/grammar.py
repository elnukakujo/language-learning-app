from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..base import BaseFeatureModel

class Grammar(BaseFeatureModel):
    __tablename__ = 'grammar'
    
    title = Column(String, index=True)
    explanation = Column(String)
    
    # Relations
    learnable_sentences = relationship(                 # 1 to Many
        'Passage',
        back_populates='grammar',
        cascade='all, delete-orphan'
    )
    
    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict = {
            **super().to_dict(include_relations=include_relations),
            "title": self.title,
            "explanation": self.explanation
        }
        if include_relations:
            base_dict.update({
                "learnable_sentences_ids": [p.id for p in self.learnable_sentences]
            })
        return base_dict