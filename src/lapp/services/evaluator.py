import numpy as np
from scipy.spatial.distance import cosine
import language_tool_python
from sqlalchemy.orm import Session
from typing import Optional
import torchaudio
import math

import logging
logger = logging.getLogger(__name__)

from ..core.database import db_manager
from ..utils import (
    detect_text_language,
    load_spacy_model,
    text_embedding_model,
    audio_embedding_model,
    audio_embedding_processor,
    stt_pipe
)
from .features import ExerciseService

exercise_service = ExerciseService()

class EvaluatorService:
    text_embedding_model = text_embedding_model
    
    audio_embedding_model = audio_embedding_model
    audio_embedding_processor = audio_embedding_processor

    stt_pipe = stt_pipe

    exercises_scales = {
        "translate": (0.6, 0.2, 0.2),
        "organize": (0.5, 0.1, 0.4),
        "type_in_the_blank": (0.5, 0.1, 0.4),
        "essay": (0.4, 0.4, 0.2),
        "answering": (0.6, 0.3, 0.1),
        "speaking": (0.3, 0.1, 0.6),
        "conversation": (0.5, 0.3, 0.2)
    }

    exercises_thresholds = {
        "speaking":0.70,
        "type_in_the_blank":0.70,
        "organize":0.65,
        "translate":0.60,
        "answering":0.55,
        "conversation":0.50,
        "essay":0.45
    }

    grammar_fallback_score = 1.0

    def _get_correct_text_and_type(self, ex_id: str, session: Optional[Session]) -> tuple[Optional[str], Optional[str]]:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            exercise = exercise_service.get_by_id(ex_id, session=session)
            
            if not exercise:
                logger.warning(f"Exercise item not found: {ex_id}")
                return False, None
            
            if not exercise.exercise_type in ['translate', 'essay', 'organize', 'answering', 'type_in_the_blank']:
                logger.warning(f"Exercise item {ex_id} is not a translation exercise")
                return False, None
            
            return exercise.answer, exercise.exercise_type
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to retrieve correct text for Exercise {ex_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def _get_correct_audio_path_and_type(self, ex_id: str, correct_audio_index: int, session: Optional[Session]) -> tuple[Optional[str], Optional[str]]:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            exercise = exercise_service.get_by_id(ex_id, session=session)
            
            if not exercise:
                logger.warning(f"Exercise item not found: {ex_id}")
                return False, None
            
            if not exercise.exercise_type in ['speaking', 'conversation']:
                logger.warning(f"Exercise item {ex_id} is not a speaking exercise")
                return False, None
            
            if not exercise.audio_files:
                logger.warning(f"Exercise item {ex_id} has no audio files")
                return False, None

            from .media import MediaService
            media_service = MediaService()

            _, correct_speaking_path = media_service.get_file_path("/".join(exercise.audio_files[correct_audio_index].split("/")[2:]))

            return correct_speaking_path, exercise.exercise_type
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to retrieve correct audio path for Exercise {ex_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def _extract_waveform_from_path(self, audio_path: str) -> np.ndarray:
        waveform, sr = torchaudio.load(audio_path)
        if sr != 16000:
            waveform = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)(waveform)
        return waveform.mean(dim=0).numpy()
    
    def _speech_to_embeddings(self, waveform: np.ndarray) -> list[float]:
        input_processed = self.audio_embedding_processor(waveform, sampling_rate=16000, return_tensors="pt", padding=True)
        return self.audio_embedding_model(**input_processed, output_hidden_states=True).hidden_states[-1].squeeze(0).mean(dim=0).detach().numpy()
    
    def _speech_to_text(self, waveform: np.ndarray) -> str:
        return self.stt_pipe(waveform, return_timestamps=False)["text"]

    def _compute_cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        return float(1-cosine(u = vec1, v = vec2))

    def _compute_grammar_error_rate(self, user_translation: str, correct_translation: str) -> float:
        language = detect_text_language(correct_translation)
        try:
            tool = language_tool_python.LanguageTool(language.iso1)
            matches = tool.check(user_translation)
        except Exception as err:
            logger.warning(
                f"LanguageTool check failed for language '{language.iso1}'. "
                f"Using fallback grammar score {self.grammar_fallback_score:.2f}. Error: {err}"
            )
            return self.grammar_fallback_score

        WHITESPACE_RULE_IDS = {
            "WHITESPACE_BEFORE_PUNCTUATION",
            "WHITESPACE_AFTER_PUNCTUATION", 
            "DOUBLE_WHITESPACE",
            "WHITESPACE_RULE",
            "TYPOGRAPHY_RULE",
        }

        substantive_errors = [
            m for m in matches
            if m.rule_id not in WHITESPACE_RULE_IDS
            and not "WHITESPACE" in m.rule_id
            and m.category != "MISC"
        ]

        num_errors = len(substantive_errors)
        score = math.exp(-0.4 * num_errors)
        logger.info(
            f"Grammar check for '{user_translation}': "
            f"{len(matches)} raw → {num_errors} substantive errors → score {score:.3f} "
            f"(filtered: {[m.rule_id for m in matches if m not in substantive_errors]})"
        )
        logger.info(substantive_errors)
        return score
    
    def _compute_token_differences_rate(self, user_translation: str, correct_translation: str) -> float:
        language = detect_text_language(correct_translation)
        nlp = load_spacy_model(language.spacy_model)

        # Normalize whitespace for CJK languages where spaces are not meaningful
        normalized_user = user_translation.replace(" ", "") if language.iso1 in ("zh", "ja", "ko") else user_translation
        normalized_correct = correct_translation.replace(" ", "") if language.iso1 in ("zh", "ja", "ko") else correct_translation

        user_doc = nlp(normalized_user)
        correct_doc = nlp(normalized_correct)

        user_tokens = set(t.text.lower() for t in user_doc if not t.is_punct and not t.is_space)
        correct_tokens = set(t.text.lower() for t in correct_doc if not t.is_punct and not t.is_space)

        if not user_tokens:
            return 1.0 if not correct_tokens else 0.5

        common_tokens = correct_tokens.intersection(user_tokens)
        return min(1, len(common_tokens) / len(user_tokens))
    
    def _evaluate_text(self, ex_id: str, user_text: str) -> dict[str, float]:
        correct_text, exercise_type = self._get_correct_text_and_type(ex_id, session=None)
        if not correct_text:
            logger.warning(f"Could not retrieve correct text for Exercise {ex_id}. Returning score of 0.")
            raise ValueError("Correct text not found for the given exercise ID.")

        # Get the weights for the specific exercise type
        x, y, z = self.exercises_scales[exercise_type]

        embedding_similarity = self._compute_cosine_similarity(
            self.text_embedding_model.encode(user_text),
            self.text_embedding_model.encode(correct_text)
        )
        logger.info(f"Embedding similarity for Exercise {ex_id}between user: '{user_text}' and correct answer: '{correct_text}' is {embedding_similarity:.4f}")
        
        grammar_error_rate = self._compute_grammar_error_rate(user_text, correct_text)
        logger.info(f"Grammar error rate for Exercise {ex_id} for user text: '{user_text}' is {grammar_error_rate:.4f}") 

        token_difference_rate = self._compute_token_differences_rate(user_text, correct_text)
        logger.info(f"Token difference rate for Exercise {ex_id} between user: '{user_text}' and correct answer: '{correct_text}' is {token_difference_rate:.4f}")

        return {
            "score": x * embedding_similarity + y * grammar_error_rate + z * token_difference_rate,
            "similarity": embedding_similarity,
            "grammar_error_rate": grammar_error_rate,
            "token_difference_rate": token_difference_rate
        }
    
    def _evaluate_speech(self, ex_id: str, user_audio_path: str, correct_audio_index: int) -> dict[str, float]:
        correct_audio_path, exercise_type = self._get_correct_audio_path_and_type(ex_id, correct_audio_index, session=None)
        if not correct_audio_path:
            logger.warning(f"Could not retrieve correct audio path for Exercise {ex_id}. Returning score of 0.")
            raise ValueError("Correct audio path not found for the given exercise ID.")
        
        from .media import MediaService
        media_service = MediaService()
        _, user_audio_path = media_service.get_file_path(user_audio_path)

        logger.info(f"Evaluating speech for Exercise {ex_id} with user audio: '{user_audio_path}' and correct audio: '{correct_audio_path}'")

        correct_waveform = self._extract_waveform_from_path(correct_audio_path)
        user_waveform = self._extract_waveform_from_path(user_audio_path)
        
        embedding_similarity = self._compute_cosine_similarity(
            self._speech_to_embeddings(user_waveform),
            self._speech_to_embeddings(correct_waveform)
        )

        user_transcription = self._speech_to_text(user_waveform)
        correct_transcription = self._speech_to_text(correct_waveform)
        logger.info(f"Transcribed user audio for Exercise {ex_id}: '{user_transcription}'")
        logger.info(f"Transcribed correct audio for Exercise {ex_id}: '{correct_transcription}'")

        grammar_error_rate = self._compute_grammar_error_rate(
            user_transcription,
            correct_transcription
        )

        token_difference_rate = self._compute_token_differences_rate(
            user_transcription,
            correct_transcription
        )

        # Get the weights for the specific exercise type
        x, y, z = self.exercises_scales[exercise_type]

        return {
            "score": x * embedding_similarity + y * grammar_error_rate + z * token_difference_rate,
            "similarity": embedding_similarity,
            "grammar_error_rate": grammar_error_rate,
            "token_difference_rate": token_difference_rate
        }

    def evaluate(self, ex_id: str, user_input: str, input_type: str, correct_audio_index: int = 0) -> float:
        """
        Evaluate a user's answer for a given exercise ID and input type (text or speech).
        
        Args:
            - ex_id: The ID of the exercise to evaluate.
            - user_input: The user's answer, either as text or a path to an audio file.
            - input_type: The type of input, either 'text' or 'speech'.
            - threshold: The score threshold above which the answer is considered correct (default is 0.8).
            - correct_audio_index: For speech evaluation, the index of the correct audio file to compare against (default is 0).
            
        Returns:
            A dictionary containing:
                - 'correct': A boolean indicating whether the answer is correct based on the threshold.
                - 'score': The computed score for the user's answer.
                - 'feedback': A string with feedback for the user (currently empty, to be implemented).      
        """
        if input_type == 'text':
            results = self._evaluate_text(ex_id, user_input)
        elif input_type == 'speech':
            results = self._evaluate_speech(ex_id, user_input, correct_audio_index=correct_audio_index)
        else:
            logger.warning(f"Invalid input type '{input_type}' for evaluation. Returning score of 0.")
            raise ValueError("Invalid input type for evaluation. Must be 'text' or 'speech'.")
        
        logger.info(f"Evaluation results for Exercise {ex_id} with input type '{input_type}': {results}")
        threshold = self.exercises_thresholds.get(exercise_service.get_by_id(ex_id, session=None).exercise_type, 0.5)
        return {
            "correct": results["score"] > threshold,
            "score": results["score"],
            "feedback": "" ## TODO
        }