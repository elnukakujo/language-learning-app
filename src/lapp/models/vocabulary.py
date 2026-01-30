from sqlalchemy import Column, String

from .base import BaseComponentModel

class Vocabulary(BaseComponentModel):
    __tablename__ = 'vocabulary'
    
    word = Column(String, index=True)
    translation = Column(String)
    phonetic = Column(String, default="")
    example_sentence = Column(String, default="")
    type = Column(String, default="")  # e.g., noun, verb, adjective
    
    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(include_relations=include_relations),
            "word": self.word,
            "translation": self.translation,
            "phonetic": self.phonetic,
            "example_sentence": self.example_sentence,
            "type": self.type
        }
        return base_dict