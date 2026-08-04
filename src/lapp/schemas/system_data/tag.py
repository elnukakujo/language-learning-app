from typing import Optional
from pydantic import BaseModel


class TagDict(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    name: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    elements: Optional[dict] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None