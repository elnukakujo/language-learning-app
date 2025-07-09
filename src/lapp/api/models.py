from datetime import date
from pydantic import BaseModel
from typing import Optional, Any

class RandomRequest(BaseModel):
    language_id: str
    unit_id: int
    type: str

class UpdatebyIdRequest(BaseModel):
    element_id: str
    updates: dict[str, Any]  # e.g. {"word": "new_word", "translation": "new_translation"}

# Pour element_type = "voc" (vocabulaire) :
#   - word, translation, phonetic, example_sentence, type
#
# Pour element_type = "gram" (règle de grammaire) :
#   - title, explanation
#
# Pour element_type = "char" (caractère calligraphié) :
#   - character, translation, components
#
# Pour element_type = "ex" (exercice) :
#   - exercise_type, question, support, answer

class NewElementRequest(BaseModel):
    language_id: str
    unit_id: int
    element_type: str  # e.g. "voc", "g", "char", "ex"
    word: Optional[str] = None
    translation: Optional[str] = None
    phonetic: Optional[str] = None
    example_sentence: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str] = None
    explanation: Optional[str] = None
    character: Optional[str] = None
    components: Optional[str] = None
    exercise_type: Optional[str] = None
    question: Optional[str] = None
    support: Optional[str] = None
    answer: Optional[str] = None

class UpdateScoreRequest(BaseModel):
    element_id: str
    success: bool