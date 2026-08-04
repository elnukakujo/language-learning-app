from sqlalchemy import Column, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from ..base import BaseComponentModel, vocabulary_example_sentence_link, grammar_example_sentence_link, calligraphy_example_sentence_link, character_passage_link, word_passage_link

class Passage(BaseComponentModel):
    __tablename__ = 'passage'
    __mapper_args__ = {"polymorphic_identity": "passage"}
    __table_args__ = (UniqueConstraint('language_id', 'text', name='uq_passage_language_text'),)
    
    text = Column(Text, nullable=False)
    translation = Column(Text, nullable=True)

    # Relationship
    vocabulary = relationship(
        'Vocabulary',
        secondary=vocabulary_example_sentence_link,
        back_populates='example_sentences'
    )
    grammar = relationship(
        'Grammar',
        secondary=grammar_example_sentence_link,
        back_populates='example_sentences'
    )
    calligraphy = relationship(
        'Calligraphy',
        secondary=calligraphy_example_sentence_link,
        back_populates='example_sentences'
    )
    characters = relationship(
        'Character',
        secondary=character_passage_link,
        back_populates='passages'
    )
    words = relationship(
        'Word',
        secondary=word_passage_link,
        back_populates='passages'
    )

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(include_relations=False),
            "text": self.text,
            "translation": self.translation
        }
        if include_relations:
            base_dict.update({
                "vocabulary": [v.to_dict(include_relations=False) for v in self.vocabulary],
                "grammar": [g.to_dict(include_relations=False) for g in self.grammar],
                "calligraphy": [cf.to_dict(include_relations=False) for cf in self.calligraphy],
                "characters": [c.to_dict(include_relations=False) for c in self.characters],
                "words": [w.to_dict(include_relations=False) for w in self.words]
            })
        return base_dict