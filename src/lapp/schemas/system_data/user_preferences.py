from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class UserPreferencesDict(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    native_language_iso639_2: Optional[List[str]] = ['eng']
    learning_goals: Optional[str] = ''
    preferred_exercise_types: Optional[List[str]] = []
    daily_goal_minutes: Optional[int] = 20
    last_updated: Optional[datetime] = None
    user: Optional[dict] = None