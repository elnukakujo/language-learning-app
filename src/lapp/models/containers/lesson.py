from sqlalchemy import Column, String, ForeignKey, Computed
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..base import BaseContainerModel

class Lesson(BaseContainerModel):
    __tablename__ = 'lesson'
    __mapper_args__ = {"polymorphic_identity": "lesson"}

    title = Column(String, index=True)

    # Overrides BaseElementModel.status: lesson uses the feature-style
    # thresholds (0/75/100), not the container/language thresholds.
    status = Column(
        String,
        Computed("CASE WHEN score = 0 THEN 'unstarted' WHEN score < 75 THEN 'inprogress' WHEN score < 100 THEN 'revisiting' ELSE 'completed' END"),
        nullable=False
    )

    # Foreign key
    language_id: Mapped[str] = mapped_column(ForeignKey('language.id'))

    # Relationships
    language: Mapped["Language"] = relationship(
        "Language",
        back_populates="lessons",
        foreign_keys=[language_id],
    )
    calligraphy: Mapped[list["Calligraphy"]] = relationship(
        "Calligraphy",
        back_populates="lesson",
        cascade="all, delete-orphan"
    )
    grammar: Mapped[list["Grammar"]] = relationship(
        "Grammar",
        back_populates="lesson",
        cascade="all, delete-orphan"
    )
    vocabulary: Mapped[list["Vocabulary"]] = relationship(
        "Vocabulary",
        back_populates="lesson",
        cascade="all, delete-orphan"
    )
    exercise: Mapped[list["Exercise"]] = relationship(
        "Exercise",
        back_populates="lesson",
        cascade="all, delete-orphan"
    )

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(include_relations=include_relations),
            "title": self.title
        }

        if include_relations:
            base_dict.update({
                "language_id": self.language_id,
                "calligraphy": [calligraphy.id for calligraphy in self.calligraphy],
                "grammar": [grammar.id for grammar in self.grammar],
                "vocabulary": [vocab.id for vocab in self.vocabulary],
                "exercise_ids": [ex.id for ex in self.exercise]
            })
        return base_dict