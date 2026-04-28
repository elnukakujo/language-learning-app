from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from ..base import BaseContainerModel
from .lesson import Lesson

class Language(BaseContainerModel):
    __tablename__ = 'language'

    user_id = Column(String, ForeignKey('user.id'), nullable=False, default='user_0')

    name = Column(String, index=True)
    native_name = Column(String)
    level = Column(String)
    description = Column(String, default="")
    flag = Column(String, default="")
    current_lesson = Column(String, ForeignKey('lesson.id'), nullable=True)

    # One-to-many: all lessons belonging to this language
    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson",
        back_populates="language",
        cascade="all, delete-orphan",
        foreign_keys=[Lesson.language_id],
    )

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(),
            "name": self.name,
            "user_id": self.user_id,
            "native_name": self.native_name,
            "level": self.level,
            "description": self.description,
            "flag": self.flag,
            "current_lesson": self.current_lesson,
        }

        if include_relations:
            base_dict.update({
                "lesson_ids": [lesson.id for lesson in self.lessons],
            })
        
        return base_dict