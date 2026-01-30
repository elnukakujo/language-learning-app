from sqlalchemy import Column, String

from .base import BaseComponentModel

class Character(BaseComponentModel):
    __tablename__ = 'character'

    character = Column(String, index=True)  # e.g., the character itself
    components = Column(String, default="")
    phonetic = Column(String)  # e.g., pinyin for Chinese characters
    meaning = Column(String)
    example_word = Column(String, default="")

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict = {
            **super().to_dict(include_relations=include_relations),
            "character": self.character,
            "components": self.components,
            "phonetic": self.phonetic,
            "meaning": self.meaning,
            "example_word": self.example_word,
        }

        return base_dict