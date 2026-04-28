from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..base import BaseFeatureModel, exercise_calligraphy_link, exercise_grammar_link, exercise_vocabulary_link

class Exercise(BaseFeatureModel):
    __tablename__ = 'exercise'

    exercise_type = Column(String, index=True)  # e.g., multiple choice, fill
    question = Column(String, index=True)
    answer = Column(String)
    text_support = Column(String, default="")   # e.g., additional text information
    
    vocabulary = relationship('Vocabulary', secondary=exercise_vocabulary_link)
    calligraphy = relationship('Calligraphy', secondary=exercise_calligraphy_link)
    grammar = relationship('Grammar', secondary=exercise_grammar_link)
    
    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict = {
            **super().to_dict(include_relations=include_relations),
            "exercise_type": self.exercise_type,
            "question": self.question,
            "text_support": self.text_support,
            "answer": self.answer,
            "vocabulary_ids": [v.id for v in self.vocabulary],
            "calligraphy_ids": [c.id for c in self.calligraphy],
            "grammar_ids": [g.id for g in self.grammar],
        }
        return base_dict