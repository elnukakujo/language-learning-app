from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from ..base import BaseComponentModel, character_word_link, character_passage_link

class Character(BaseComponentModel):
    __tablename__ = 'character'
    __mapper_args__ = {"polymorphic_identity": "character"}
    __table_args__ = (UniqueConstraint('language_id', 'character', name='uq_character_language_character'),)
    
    character = Column(String, nullable=False, index=True)
    phonetic = Column(String, nullable=False)
    meaning = Column(String, nullable=True)
    radical = Column(String, nullable=True)
    strokes = Column(Integer, nullable=True)
    
    # Relationship
    calligraphy = relationship('Calligraphy', back_populates='character')  # One to One

    words = relationship(
        'Word',
        secondary=character_word_link,
        back_populates='characters'
    )
    passages = relationship(
        'Passage',
        secondary=character_passage_link,
        back_populates='characters'
    )

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(include_relations=False),
            "character": self.character,
            "meaning": self.meaning,
            "phonetic": self.phonetic,
            "radical": self.radical,
            "strokes": self.strokes
        }
        if include_relations:
            base_dict.update({
                "calligraphy": [c.to_dict(include_relations=False) for c in self.calligraphy],
                "words": [w.to_dict(include_relations=False) for w in self.words],
                "passages": [p.to_dict(include_relations=False) for p in self.passages]
            })
        return base_dict