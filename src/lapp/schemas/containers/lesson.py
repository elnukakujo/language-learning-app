from typing import Optional

from ..base import BaseContainerDict

class LessonDict(BaseContainerDict):
    user_id: Optional[str] = None
    language_id: str
    title: str