from datetime import date
from typing import Optional
from pydantic import BaseModel


class SourceDict(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    title: Optional[str] = None
    date: Optional[date] = None
    description: Optional[str] = None
    source_type: Optional[str] = None

