from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from ..base import BaseFeatureModel, calligraphy_example_word_link

class Calligraphy(BaseFeatureModel):
    __tablename__ = 'calligraphy'

    # Foreign keys
    character_id = Column(String, ForeignKey('character.id'), nullable=False, unique=False)

    # Relations
    character = relationship(                       # One to One
        'Character',
        back_populates='calligraphy'
    )  
    example_words = relationship(
        'Word',
        secondary=calligraphy_example_word_link,
        back_populates='calligraphy'
    )

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict = {
            **super().to_dict(include_relations=include_relations),
            "character": self.character.to_dict(include_relations=False),
            "example_word": self.example_words[0].to_dict(include_relations=False) if self.example_words else None,
            "example_word_ids": [word.id for word in self.example_words],
        }

        return base_dict