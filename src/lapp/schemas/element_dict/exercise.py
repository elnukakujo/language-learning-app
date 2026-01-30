from typing import Optional
from pydantic import model_validator

from .base import BaseComponentDict

class ExerciseDict(BaseComponentDict):
    exercise_type: Optional[str] = None         # e.g., "fill_in_the_blank", "multiple_choice"
    question: str
    answer: str
    text_support: Optional[str] = None          # e.g., additional text information

    vocabulary_ids: Optional[list[str]] = None # e.g., ["voc_V1"]
    character_ids: Optional[list[str]] = None  # e.g., ["char_C1"]
    grammar_ids: Optional[list[str]] = None    # e.g., ["gram_G1"]

    @model_validator(mode='after')
    def _validate(self):
        valid_exercise_types = [
            "essay",
            "answering",
            "translate",
            "organize",
            "fill_in_the_blank",
            "matching",
            "true_false"
        ]
        if self.exercise_type not in valid_exercise_types:
            raise ValueError(f"Invalid exercise_type: {self.exercise_type}. Must be one of {valid_exercise_types}.")
        return self