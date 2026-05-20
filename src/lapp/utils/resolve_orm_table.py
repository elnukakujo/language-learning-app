from typing import Optional, Type

def resolve_element_model(element_id: str) -> Optional[Type]:
        """Map an element id string to the corresponding ORM model.
        
        ID Format:
        - Language: "lang_L{n}"
        - Lesson: "lesson_L{n}"
        - Vocabulary: "voc_V{n}"
        - Grammar: "gram_G{n}"
        - Calligraphy: "call_C{n}"
        - Exercise: "ex_E{n}"
        - Character: "char_C{n}"
        - Word: "word_W{n}"
        - Passage: "pass_P{n}"
        """
        from ..models.features import Vocabulary, Grammar, Calligraphy, Exercise
        from ..models.components import Word, Passage, Character
        from ..models.containers import Language, Lesson
        from ..models.system_data import Tag, Source, User, StrengthsAndWeaknesses, UserPreferences
        from ..models.data_collection import ProgressTracking
        model_map = {
            "lang": Language,
            "lesson": Lesson,
            "voc": Vocabulary,
            "gram": Grammar,
            "call": Calligraphy,
            "ex": Exercise,
            "char": Character,
            "word": Word,
            "pass": Passage,
            "user": User,
            "pref": UserPreferences,
            "src": Source,
            "tag": Tag,
            "sw": StrengthsAndWeaknesses,
            "pt": ProgressTracking,
        }
        return model_map.get(element_id.split("_")[0])