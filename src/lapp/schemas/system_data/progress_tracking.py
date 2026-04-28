from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProgressTrackingDict(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    language_id: Optional[str] = None
    language_name: Optional[str] = None
    element_type: Optional[str] = None
    element_status: Optional[str] = None
    new_score_difference: Optional[int] = None
    created_at: Optional[datetime] = None
    n_reviewed: Optional[int] = 1

