from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime

# High-level base schemas for languages and lessons containers
class BaseContainerDict(BaseModel):
    id: Optional[str] = None
    score: Optional[float] = 0.0
    created_at: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    last_seen_at: Optional[datetime] = None

    @model_validator(mode="after")
    def _sync_last_seen(self):
        if self.last_seen is None and self.last_seen_at is not None:
            self.last_seen = self.last_seen_at
        if self.last_seen_at is None and self.last_seen is not None:
            self.last_seen_at = self.last_seen
        return self

# Middle-level base schema for features like Vocabulary, Grammar, Calligraphy, Exercise
class BaseFeatureDict(BaseContainerDict):
    lesson_id: Optional[str] = None
    lesson_id: Optional[str] = None
    image_files: Optional[list[str]] = None     # e.g. list of image file paths
    audio_files: Optional[list[str]] = None     # e.g. list of audio file paths

    @model_validator(mode="after")
    def _validate_container_id(self):
        if self.lesson_id is None and self.lesson_id is not None:
            self.lesson_id = self.lesson_id
        if self.lesson_id is None and self.lesson_id is not None:
            self.lesson_id = self.lesson_id
        if not self.lesson_id:
            raise ValueError("Either lesson_id or lesson_id is required")
        return self

# Low-level base schema for Calligraphy, Word, and Passage components
class BaseComponentDict(BaseModel):
    id: Optional[str] = None
    language_id: Optional[str] = None
    score: Optional[float] = 0.0
    created_at: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    last_seen_at: Optional[datetime] = None
    image_files: Optional[list[str]] = None
    audio_files: Optional[list[str]] = None