from typing import Optional
from pydantic import model_validator

from ..base import BaseFeatureDict
from .vocabulary import VocabularyDict
from .calligraphy import CalligraphyDict
from .grammar import GrammarDict

class ExerciseDict(BaseFeatureDict):
    exercise_type: Optional[str] = None         # e.g., "type_in_the_blank", "multiple_choice"
    question: str
    answer: str
    text_support: Optional[str] = None          # e.g., additional text information

    related_vocabulary: Optional[list[VocabularyDict]] = None # e.g., ["voc_V1"]
    related_calligraphy: Optional[list[CalligraphyDict]] = None  # e.g., ["call_C1"]
    related_grammar: Optional[list[GrammarDict]] = None    # e.g., ["gram_G1"]

    @model_validator(mode='after')
    def _validate(self):
        valid_exercise_types = [
            "essay",
            "answering",
            "translate",
            "organize",
            "type_in_the_blank",
            "select_in_the_blank",
            "matching",
            "true_false",
            "speaking",
            "conversation",
        ]
        if self.exercise_type not in valid_exercise_types:
            raise ValueError(f"Invalid exercise_type: {self.exercise_type}. Must be one of {valid_exercise_types}.")
        return self