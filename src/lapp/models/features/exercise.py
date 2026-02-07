from sqlalchemy import Column, String, JSON

from ..base import BaseFeatureModel

class Exercise(BaseFeatureModel):
    __tablename__ = 'exercise'

    exercise_type = Column(String, index=True)  # e.g., multiple choice, fill
    question = Column(String, index=True)
    answer = Column(String)
    text_support = Column(String, default="")   # e.g., additional text information
    
    # Store relationship IDs as JSON arrays
    vocabulary_ids = Column(JSON, default=list)
    calligraphy_ids = Column(JSON, default=list)
    grammar_ids = Column(JSON, default=list)
    
    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict = {
            **super().to_dict(include_relations=include_relations),
            "exercise_type": self.exercise_type,
            "question": self.question,
            "text_support": self.text_support,
            "answer": self.answer,
            "vocabulary_ids": self.vocabulary_ids,
            "calligraphy_ids": self.calligraphy_ids,
            "grammar_ids": self.grammar_ids
        }
        return base_dict