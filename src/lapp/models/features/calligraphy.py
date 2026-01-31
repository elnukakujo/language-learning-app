from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..base import BaseFeatureModel

class Calligraphy(BaseFeatureModel):
    __tablename__ = 'calligraphy'

    # Foreign keys
    character_id = Column(Integer, ForeignKey('character.id'), nullable=False, unique=True)
    example_word_id = Column(Integer, ForeignKey('word.id'), nullable=True, unique=False)

    # Relations
    character = relationship(                       # One to One
        'Character'
    )  
    example_word = relationship(                    # Many to One
        'Word',
        back_populates='calligraphy'
    )

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict = {
            **super().to_dict(include_relations=include_relations),
            **self.character.to_dict(include_relations=include_relations),
            **self.example_word.to_dict(include_relations=include_relations)
        }

        return base_dict