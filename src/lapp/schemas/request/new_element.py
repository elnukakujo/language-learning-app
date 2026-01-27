from .base import BaseRequest
from ..element_dict import (
    VocabularyDict,
    GrammarDict,
    CharacterDict,
    ExerciseDict,
    UnitDict,
    LanguageDict,
)

class NewElementRequest(BaseRequest):
    element_type: str
    element: VocabularyDict | GrammarDict | CharacterDict | ExerciseDict | UnitDict | LanguageDict