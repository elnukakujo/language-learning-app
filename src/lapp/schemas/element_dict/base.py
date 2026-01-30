from pydantic import BaseModel
from typing import Optional
from datetime import date

class BaseElementDict(BaseModel):
    id: Optional[str] = None
    score: Optional[float] = 0.0
    last_seen: Optional[date] = date.today()

class BaseComponentDict(BaseElementDict):
    unit_id: str
    image_files: Optional[list[str]] = None     # e.g. list of image file paths
    audio_files: Optional[list[str]] = None     # e.g. list of audio file paths