from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BaseElementDict(BaseModel):
    id: Optional[str] = None
    score: Optional[float] = 0.0
    created_at: Optional[datetime] = None
    last_seen_at: Optional[datetime] = None
    status: Optional[str] = None

class BaseModelWithMediaFiles(BaseModel):
    image_files: list[str]     # e.g. list of image file paths
    audio_files: list[str]     # e.g. list of audio file paths

# High-level base schemas for languages and lessons containers
class BaseContainerDict(BaseElementDict):
    level: Optional[str] = None
    description: Optional[str] = None

# Middle-level base schema for features like Vocabulary, Grammar, Calligraphy, Exercise
class BaseFeatureDict(BaseElementDict, BaseModelWithMediaFiles):
    lesson_id: Optional[str] = None
    difficulty: Optional[str] = None

# Low-level base schema for Calligraphy, Word, and Passage components
class BaseComponentDict(BaseElementDict, BaseModelWithMediaFiles):
    language_id: Optional[str] = None
    difficulty: Optional[str] = None