from typing import Optional
from pydantic import model_validator

from ..base import BaseContainerDict

class LessonDict(BaseContainerDict):
    user_id: Optional[str] = "user_0"
    language_id: str
    lesson_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    level: Optional[str] = "A1"  # Default level

    @model_validator(mode="after")
    def _sync_lesson_id(self):
        if self.lesson_id is None and self.id is not None:
            self.lesson_id = self.id
        return self