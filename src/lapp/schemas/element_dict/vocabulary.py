from typing import Optional

from .base import BaseElementDict

class VocabularyDict(BaseElementDict):
    unit_id: str
    word: str
    translation: str
    phonetic: Optional[str] = None  # e.g., pinyin for Chinese words
    example_sentence: Optional[str] = None  # Example sentence using the word
    type: Optional[str] = None # e.g., noun, verb, adjective