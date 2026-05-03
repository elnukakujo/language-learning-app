from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from ..base import BaseComponentModel

class Character(BaseComponentModel):
    __tablename__ = 'character'
    __table_args__ = (UniqueConstraint('language_id', 'character', name='uq_character_language_character'),)
    
    character = Column(String, nullable=False, index=True)
    phonetic = Column(String, nullable=False)
    meaning = Column(String, nullable=True)
    radical = Column(String, nullable=True)
    strokes = Column(Integer, nullable=True)
    
    # Relationship
    calligraphy = relationship('Calligraphy', back_populates='character')  # One to One

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(),
            "character": self.character,
            "meaning": self.meaning,
            "phonetic": self.phonetic,
            "radical": self.radical,
            "strokes": self.strokes
        }
        if include_relations:
            base_dict.update({
                "calligraphy": [c.id for c in self.calligraphy]
            })
        return base_dict