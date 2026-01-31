from pydantic import BaseModel
from typing import Optional
from datetime import date

# High-level base schemas for languages and units containers
class BaseContainerDict(BaseModel):
    id: Optional[str] = None
    score: Optional[float] = 0.0
    last_seen: Optional[date] = date.today()

# Middle-level base schema for features like Vocabulary, Grammar, Calligraphy, Exercise
class BaseFeatureDict(BaseContainerDict):
    unit_id: str
    image_files: Optional[list[str]] = None     # e.g. list of image file paths
    audio_files: Optional[list[str]] = None     # e.g. list of audio file paths

# Low-level base schema for Calligraphy, Word, and Passage components
class BaseComponentDict(BaseModel):
    id: Optional[str] = None
    image_files: Optional[list[str]] = None
    audio_files: Optional[list[str]] = None