from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import relationship

from ..base import BaseComponentModel, calligraphy_example_word_link, grammar_example_word_link, character_word_link, word_passage_link

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

    characters = relationship(
        'Character',
        secondary=character_word_link,
        back_populates='words'
    )
    passages = relationship(
        'Passage',
        secondary=word_passage_link,
        back_populates='words'
    )

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(include_relations=False),
            "word": self.word,
            "translation": self.translation,
            "phonetic": self.phonetic,
            "word_type": self.word_type,
            "word_gender": self.word_gender,
        }
        if include_relations:
            base_dict.update({
                "vocabulary": [v.to_dict(include_relations=False) for v in self.vocabulary],
                "grammar": [g.to_dict(include_relations=False) for g in self.grammar],
                "calligraphy": [cf.to_dict(include_relations=False) for cf in self.calligraphy],
                "characters": [c.to_dict(include_relations=False) for c in self.characters],
                "passages": [p.to_dict(include_relations=False) for p in self.passages]
            })
        return base_dict