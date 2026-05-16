from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from ..base import BaseContainerModel
from .lesson import Lesson

class Language(BaseContainerModel):
    __tablename__ = 'language'
    __mapper_args__ = {"polymorphic_identity": "language"}

    name = Column(String, index=True)
    alias = Column(String)
    flag = Column(String, default="")

    source_iso639_2t = Column(String, nullable=True)
    target_iso639_2t = Column(String, nullable=True)

    # Foreign keys
    current_lesson_id = Column(String, ForeignKey('lesson.id'), nullable=True)

    # One-to-many: all lessons belonging to this language
    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson",
        back_populates="language",
        cascade="all, delete-orphan",
        foreign_keys=[Lesson.language_id],
    )

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(include_relations),
            "name": self.name,
            "alias": self.alias,
            "flag": self.flag,
            "source_iso639_2t": self.source_iso639_2t,
            "target_iso639_2t": self.target_iso639_2t,
        }

        if include_relations:
            base_dict.update({
                "current_lesson_id": self.current_lesson_id,
                "lesson_ids": [lesson.id for lesson in self.lessons],
            })
        
        return base_dict