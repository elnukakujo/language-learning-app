from typing import Optional
from pydantic import BaseModel, model_validator


class SourceDict(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    title: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
    source_type: Optional[str] = None
    elements: Optional[dict] = None

    @model_validator(mode="before")
    def validate_source_type(cls, values):
        source_type = values.get("source_type")
        if source_type and source_type not in ["original", "textbook", "class", "online", "media", "social", "other", "ai"]:
            raise ValueError(f"Invalid source_type: {source_type}")
        return values