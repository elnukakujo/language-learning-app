from typing import Optional

from ..base import BaseContainerDict

class LanguageDict(BaseContainerDict):
    name: str
    native_name: Optional[str] = None
    level: Optional[str] = "A1"  # Default level
    description: Optional[str] = None
    flag: Optional[str] = None  # Flag emoji
    current_unit: Optional[str] = None