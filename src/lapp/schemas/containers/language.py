from typing import Optional

from ..base import BaseContainerDict

class LanguageDict(BaseContainerDict):
    user_id: Optional[str] = None
    name: str
    native_name: Optional[str] = None
    flag: Optional[str] = None  # Flag emoji
    current_lesson_id: Optional[str] = None