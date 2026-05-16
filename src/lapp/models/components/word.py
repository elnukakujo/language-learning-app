from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import relationship

from ..base import BaseComponentModel, calligraphy_example_word_link, grammar_example_word_link

class Word(BaseComponentModel):
    __tablename__ = 'word'
    __mapper_args__ = {"polymorphic_identity": "word"}
    __table_args__ = (UniqueConstraint('language_id', 'word', name='uq_word_language_word'),)
    
    word = Column(String(255), nullable=False, index=True)
    translation = Column(String(500), nullable=False)
    phonetic = Column(String(255), nullable=True)
    word_type = Column(String(100), nullable=True)
    word_gender = Column(String(50), nullable=True)
    
    # Relationship
    vocabulary = relationship('Vocabulary', back_populates='word')      # One to Many

    grammar = relationship(
        'Grammar',
        secondary=grammar_example_word_link,
        back_populates='example_words'
    )

    calligraphy = relationship(
        'Calligraphy',
        secondary=calligraphy_example_word_link,
        back_populates='example_words'
    )

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(),
            "word": self.word,
            "translation": self.translation,
            "phonetic": self.phonetic,
            "word_type": self.word_type,
            "word_gender": self.word_gender,
        }
        if include_relations:
            base_dict.update({
                "vocabulary": [v.id for v in self.vocabulary],
                "grammar": [g.id for g in self.grammar],
                "calligraphy": [cf.id for cf in self.calligraphy]
            })
        return base_dict