from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, field_validator

class UserPreferencesDict(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    native_language_iso639_2: Optional[List[str]] = ['eng']
    learning_goals: Optional[str] = ''
    preferred_exercise_types: Optional[List[str]] = []
    daily_goal_minutes: Optional[int] = 20
    last_updated: Optional[datetime] = None
    ai_feedback_enabled: Optional[bool] = True
    ai_learnable_sentence_enabled: Optional[bool] = True
    ai_example_sentence_enabled: Optional[bool] = True
    ai_example_word_enabled: Optional[bool] = True
    ai_tts_enabled: Optional[bool] = True
    ai_gen_api_base_url: Optional[str] = None
    ai_gen_api_key: Optional[str] = None
    ai_gen_model: Optional[str] = None
    ai_tts_api_base_url: Optional[str] = None
    ai_tts_api_key: Optional[str] = None
    ai_tts_model: Optional[str] = None
    user: Optional[dict] = None

    @field_validator("ai_gen_api_base_url", "ai_tts_api_base_url")
    @classmethod
    def _validate_api_base_url(cls, value: Optional[str]) -> Optional[str]:
        if not value:
            return value
        if not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("must start with http:// or https://")
        return value.rstrip("/")