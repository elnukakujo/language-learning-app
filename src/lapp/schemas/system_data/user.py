from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserDict(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    day_streak: Optional[int] = 0
    last_review: Optional[datetime] = None
    created_at: Optional[datetime] = None

