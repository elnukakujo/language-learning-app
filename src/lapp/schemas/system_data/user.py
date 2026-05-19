from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserDict(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    last_review: Optional[datetime] = None
    created_at: Optional[datetime] = None

