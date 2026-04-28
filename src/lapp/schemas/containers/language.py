from typing import Optional

from ..base import BaseContainerDict

class LanguageDict(BaseContainerDict):
    user_id: Optional[str] = "user_0"
    name: str
    native_name: Optional[str] = None
    level: Optional[str] = "A1"  # Default level
    description: Optional[str] = None
    flag: Optional[str] = None  # Flag emoji
    current_lesson: Optional[str] = None
    current_lesson: Optional[str] = None