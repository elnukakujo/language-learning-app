from typing import Optional

from ..base import BaseContainerDict

class LessonDict(BaseContainerDict):
    title: str
    
    user_id: Optional[str] = None
    language_id: str