from sqlalchemy import Column, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from ..base import BaseComponentModel, vocabulary_example_sentence_link, grammar_example_sentence_link, calligraphy_example_sentence_link

class Passage(BaseComponentModel):
    __tablename__ = 'passage'
    __mapper_args__ = {"polymorphic_identity": "passage"}
    __table_args__ = (UniqueConstraint('language_id', 'text', name='uq_passage_language_text'),)
    
    text = Column(Text, nullable=False)
    translation = Column(Text, nullable=False)

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

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(include_relations=False),
            "text": self.text,
            "translation": self.translation
        }
        if include_relations:
            base_dict.update({
                "vocabulary": [v.id for v in self.vocabulary],
                "grammar": [g.id for g in self.grammar],
                "calligraphy": [c.id for c in self.calligraphy]
            })
        return base_dict