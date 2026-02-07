from typing import Optional
from pydantic import model_validator

from ..base import BaseComponentDict

class WordDict(BaseComponentDict):
    word: str
    translation: str
    phonetic: Optional[str] = None
    type: Optional[str] = None
    
    @model_validator(mode="after")
    def _validate(self):
        valid_types = [
            "noun",
            "verb",
            "adjective",
            "adverb",
            "pronoun",
            "article",
            "preposition",
            "conjunction",
            "particle",
            "interjection",
            "numeral",
            "classifier",
            "auxiliary",
            "modal"
        ]
        if self.type is not None and self.type.lower() not in valid_types:
            raise ValueError(f"Invalid type: {self.type}. Must be one of {valid_types}.")
        return self