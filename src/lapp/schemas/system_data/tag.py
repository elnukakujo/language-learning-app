from typing import Optional
from pydantic import BaseModel


class TagDict(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    tagged_element_type: Optional[str] = None
    name: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None

