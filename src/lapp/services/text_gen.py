
import logging
import re
logger = logging.getLogger(__name__)

from ..utils import chat_completion
from .containers import LanguageService
language_service = LanguageService()

class TextGeneratorService:
    grammar_instruct = (
        "You generate exactly one short language-learning sentence.\n"
        "Rules:\n"
        "1) Output only the sentence in TARGET language.\n"
        "2) Do not output explanations, labels, or translations.\n"
        "3) Keep the sentence simple and natural.\n"
        "4) Use the grammar point from GRAMMAR_SHEET."
    )
    grammar_shots = [
        [
            "fra",
            "zho",
            "Use 第 + number to express ordinals (first, second, third).",
            "这是我第二次来中国。"
        ],
        [
            "fra",
            "deu",
            "Use polite Sie with verb in infinitive form for formal requests.",
            "Kommen Sie bitte hierher."
        ]
    ]

    vocabulary_instruct = (
        "You generate exactly one short language-learning sentence.\n"
        "Rules:\n"
        "1) Output only the sentence in TARGET language.\n"
        "2) Do not output explanations, labels, or translations.\n"
        "3) The sentence must include VOCABULARY_WORD exactly once.\n"
        "4) Keep it simple and natural."
    )
    vocabulary_shots = [
        ["eng", "zho", "吃饭", "我喜欢吃中国饭。"],
        ["eng", "deu", "Computerspiele", "Ich spiele gern Computerspiele."]
    ]

    calligraphy_instruct = (
        "You generate exactly one target-language word for handwriting practice.\n"
        "Rules:\n"
        "1) Output only one word in TARGET language.\n"
        "2) Do not output explanations, labels, or translations.\n"
        "3) The word must contain INPUT_CHARACTER.\n"
        "4) Keep the output concise."
    )
    calligraphy_shots = [
        ["eng", "zho", "学", "学习"],
        ["eng", "zho", "语", "语言"],
        ["eng", "zho", "文", "文化"]
    ]

    @staticmethod
    def _build_user_prompt(
        task: str,
        source_lang_code: str,
        target_lang_code: str,
        input_label: str,
        input_value: str
    ) -> str:
        if not source_lang_code or not target_lang_code:
            raise ValueError(
                f"Missing language code(s): source_lang_code={source_lang_code!r}, target_lang_code={target_lang_code!r}"
            )
        return (
            f"TASK: {task}\n"
            f"SOURCE_LANG_CODE: {source_lang_code.strip().lower()}\n"
            f"TARGET_LANG_CODE: {target_lang_code.strip().lower()}\n"
            f"{input_label}:\n"
            f"{input_value}\n"
            "OUTPUT:"
        )

    def _generate_from_messages(self, messages: list[dict], max_new_tokens: int, api: dict) -> str:
        output = chat_completion(**api, messages=messages, max_tokens=max_new_tokens, disable_thinking=True).strip()
        # ponytail: defensive strip in case a reasoning model ignores the no-think instruction
        return re.sub(r"<think>.*?</think>", "", output, flags=re.DOTALL).strip()

    def generate_learnable_sentence(self, grammar_sheet: str, source_lang_code: str, target_lang_code: str, api: dict) -> str:
        """
        Generate a learnable sentence based on a grammar sheet.
        
        Args:
            grammar_sheet: The grammar sheet to use for generating the sentence.
            source_lang_code: The source language code (e.g., 'en' for English).
            target_lang_code: The target language code (e.g., 'zh' for Chinese).
        
        Returns:
            A single short example sentence that illustrates the grammar point.
        """
        if not api or not api.get("base_url"):
            logger.warning("Text Generator Service is not available. Returning empty string.")
            return ""

        system_content = self.grammar_instruct
        messages = [
            {"role": "system", "content": system_content}
        ]

        for shot_source, shot_target, grammar_shot, sentence_shot in self.grammar_shots:
            messages.append({
                "role": "user",
                "content": self._build_user_prompt(
                    task="grammar_sentence",
                    source_lang_code=shot_source,
                    target_lang_code=shot_target,
                    input_label="GRAMMAR_SHEET",
                    input_value=grammar_shot
                )
            })
            messages.append({"role": "assistant", "content": sentence_shot})

        messages.append({
            "role": "user",
            "content": self._build_user_prompt(
                task="grammar_sentence",
                source_lang_code=source_lang_code,
                target_lang_code=target_lang_code,
                input_label="GRAMMAR_SHEET",
                input_value=grammar_sheet
            )
        })

        return self._generate_from_messages(messages=messages, max_new_tokens=768, api=api)
    
    def generate_example_sentence(self, vocabulary_word: str, source_lang_code: str, target_lang_code: str, api: dict) -> str:
        """
        Generate an example sentence based on a vocabulary word.
        
        Args:
            vocabulary_word: The vocabulary word to use in the example sentence.
            source_lang_code: The source language code (e.g., 'en' for English).
            target_lang_code: The target language code (e.g., 'zh' for Chinese).
        
        Returns:
            A single short example sentence that illustrates the vocabulary word.
        """
        if not api or not api.get("base_url"):
            logger.warning("Text Generator Service is not available. Returning empty string.")
            return ""

        system_content = self.vocabulary_instruct
        messages = [
            {"role": "system", "content": system_content}
        ]

        for shot_source, shot_target, vocabulary_shot, sentence_shot in self.vocabulary_shots:
            messages.append({
                "role": "user",
                "content": self._build_user_prompt(
                    task="vocabulary_sentence",
                    source_lang_code=shot_source,
                    target_lang_code=shot_target,
                    input_label="VOCABULARY_WORD",
                    input_value=vocabulary_shot
                )
            })
            messages.append({"role": "assistant", "content": sentence_shot})

        messages.append({
            "role": "user",
            "content": self._build_user_prompt(
                task="vocabulary_sentence",
                source_lang_code=source_lang_code,
                target_lang_code=target_lang_code,
                input_label="VOCABULARY_WORD",
                input_value=vocabulary_word
            )
        })

        return self._generate_from_messages(messages=messages, max_new_tokens=768, api=api)
    
    def generate_example_word(self, character: str, source_lang_code: str, target_lang_code: str, api: dict) -> str:
        """
        Generate an example word based on a character.
        
        Args:
            character: The character to use in the example word.
            source_lang_code: The source language code (e.g., 'en' for English).
            target_lang_code: The target language code (e.g., 'zh' for Chinese).
        
        Returns:
            A single example word that contains the character.
        """
        if not api or not api.get("base_url"):
            logger.warning("Text Generator Service is not available. Returning empty string.")
            return ""

        system_content = self.calligraphy_instruct
        messages = [
            {"role": "system", "content": system_content}
        ]

        for shot_source, shot_target, calligraphy_shot, word_shot in self.calligraphy_shots:
            messages.append({
                "role": "user",
                "content": self._build_user_prompt(
                    task="calligraphy_word",
                    source_lang_code=shot_source,
                    target_lang_code=shot_target,
                    input_label="INPUT_CHARACTER",
                    input_value=calligraphy_shot
                )
            })
            messages.append({"role": "assistant", "content": word_shot})

        messages.append({
            "role": "user",
            "content": self._build_user_prompt(
                task="calligraphy_word",
                source_lang_code=source_lang_code,
                target_lang_code=target_lang_code,
                input_label="INPUT_CHARACTER",
                input_value=character
            )
        })

        return self._generate_from_messages(messages=messages, max_new_tokens=768, api=api)