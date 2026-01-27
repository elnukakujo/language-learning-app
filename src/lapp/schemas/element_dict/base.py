from pydantic import BaseModel
from typing import Optional
from datetime import date

class BaseElementDict(BaseModel):
    id: Optional[str] = None
    score: Optional[float] = 0.0
    last_seen: Optional[date] = date.today()