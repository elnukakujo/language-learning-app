from datetime import date
from typing import Optional
from pydantic import BaseModel


class StrengthsAndWeaknessesDict(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    language_id: Optional[str] = None
    element_type: Optional[str] = None
    strengths: Optional[dict] = {}
    weaknesses: Optional[dict] = {}
    embeddings: Optional[float] = None
    created_at: Optional[date] = None