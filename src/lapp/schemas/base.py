from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from .system_data import TagDict, SourceDict

class BaseElementDict(BaseModel):
    id: Optional[str] = None
    score: Optional[float] = 0.0
    created_at: Optional[datetime] = None
    last_seen_at: Optional[datetime] = None
    status: Optional[str] = None
    tags: Optional[list[TagDict]] = None
    sources: Optional[list[SourceDict]] = None

class BaseModelWithMediaFiles(BaseModel):
    image_files: Optional[list[str]] = []     # e.g. list of image file paths
    audio_files: Optional[list[str]] = []     # e.g. list of audio file paths

# High-level base schemas for languages and lessons containers
class BaseContainerDict(BaseElementDict):
    level: Optional[str] = None
    description: Optional[str] = None

# Middle-level base schema for features like Vocabulary, Grammar, Calligraphy, Exercise
class BaseFeatureDict(BaseElementDict, BaseModelWithMediaFiles):
    lesson_id: Optional[str] = None
    difficulty: Optional[float] = 0.5

# Low-level base schema for Calligraphy, Word, and Passage components
class BaseComponentDict(BaseElementDict, BaseModelWithMediaFiles):
    language_id: Optional[str] = None
    difficulty: Optional[float] = 0.5