from typing import Optional
from datetime import date

from .base import BaseElementDict

class LanguageDict(BaseElementDict):
    name: str
    native_name: Optional[str] = None
    level: Optional[str] = "A1"  # Default level
    description: Optional[str] = None
    flag: Optional[str] = None  # Flag emoji
    current_unit: Optional[str] = None