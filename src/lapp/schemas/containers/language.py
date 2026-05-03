from typing import Optional

from ..base import BaseContainerDict

class LanguageDict(BaseContainerDict):
    name: str
    alias: Optional[str] = None
    flag: Optional[str] = None  # Flag emoji

    target_iso639_2t: Optional[str] = None
    source_iso639_2t: Optional[str] = None
    
    user_id: Optional[str] = None
    current_lesson_id: Optional[str] = None