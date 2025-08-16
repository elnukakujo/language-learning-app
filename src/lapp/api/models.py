from datetime import date
from pydantic import BaseModel
from typing import Optional, Any

class LanguageDict(BaseModel):
    id: Optional[str] = None
    name: str
    native_name: Optional[str] = None
    level: Optional[str] = "A1"  # Default level
    description: Optional[str] = None
    score: Optional[float] = 0.0
    last_seen: Optional[date] = date.today()
    flag: Optional[str] = None  # Flag emoji
    current_unit: Optional[str] = None

class UnitDict(BaseModel):
    id: Optional[int] = None
    language_id: str
    title: str
    description: Optional[str] = None
    level: Optional[str] = "A1"  # Default level
    score: Optional[float] = 0.0
    last_seen: Optional[date] = date.today()

class CalligraphyCharacterDict(BaseModel):
    id: Optional[str] = None
    unit_id: str
    character: str
    components: Optional[str] = None  # Components of the character
    phonetic: str
    meaning: str
    example_word: Optional[str] = None  # Example word using the character
    score: Optional[float] = 0.0
    last_seen: Optional[date] = date.today()

class VocabularyDict(BaseModel):
    id: Optional[str] = None
    unit_id: str
    word: str
    translation: str
    phonetic: Optional[str] = None  # e.g., pinyin for Chinese words
    example_sentence: Optional[str] = None  # Example sentence using the word
    type: Optional[str] = None # e.g., noun, verb, adjective
    score: Optional[float] = 0.0
    last_seen: Optional[date] = date.today()

class GrammarRuleDict(BaseModel):
    id: Optional[str] = None
    unit_id: str
    title: str
    explanation: str
    learnable_sentence: str
    score: Optional[float] = 0.0
    last_seen: Optional[date] = date.today()

class ExerciseDict(BaseModel):
    id: Optional[str] = None 
    unit_id: str # e.g., "ZH_0"
    exercise_type: Optional[str] = None  # e.g., "fill_in_the_blank", "multiple_choice"
    question: str
    support: Optional[str] = None  # e.g., image, audio, text
    answer: str
    score: Optional[float] = 0.0
    last_seen: Optional[date] = date.today()
    associated_to: Optional[dict[str, list[str]]] = None  # e.g., {"vocabulary": ["id1", "id2"], "grammar": ["id3"], "characters": ["id4"]}

class UpdatebyIdRequest(BaseModel):
    element_id: str
    updates: dict[str, Any]  # e.g. {"word": "new_word", "translation": "new_translation"}

class NewElementRequest(BaseModel):
    element_type: str
    element: VocabularyDict | GrammarRuleDict | CalligraphyCharacterDict | ExerciseDict | UnitDict | LanguageDict

class UpdateScoreRequest(BaseModel):
    element_id: str
    success: bool