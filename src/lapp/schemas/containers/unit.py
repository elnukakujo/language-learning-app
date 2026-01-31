from typing import Optional

from ..base import BaseContainerDict

class UnitDict(BaseContainerDict):
    language_id: str
    title: str
    description: Optional[str] = None
    level: Optional[str] = "A1"  # Default level