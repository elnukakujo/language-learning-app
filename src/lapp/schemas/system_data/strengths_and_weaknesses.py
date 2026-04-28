from datetime import date
from typing import Optional
from pydantic import BaseModel


class StrengthsAndWeaknessesDict(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    language_id: Optional[str] = None
    language_name: Optional[str] = None
    element_type: Optional[str] = None
    strengths: Optional[str] = ''
    weaknesses: Optional[str] = ''
    last_updated: Optional[date] = None

