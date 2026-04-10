import numpy as np
from sentence_transformers import SentenceTransformer
import torch
from transformers import AutoProcessor, AutoModelForCTC, Wav2Vec2FeatureExtractor, Wav2Vec2Model
from scipy.spatial.distance import cosine
import language_tool_python
from sqlalchemy.orm import Session
from typing import Optional
import torchaudio

import logging
logger = logging.getLogger(__name__)

from ..core.database import db_manager
from ..utils import detect_text_language, load_spacy_model, is_offline
from .features import ExerciseService

exercise_service = ExerciseService()

class EvaluatorService:
    text_embedding_model = SentenceTransformer('all-MiniLM-L6-v2', local_files_only=is_offline())
    
    audio_embedding_model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-large-xlsr-53", local_files_only=is_offline())
    audio_embedding_processor = Wav2Vec2FeatureExtractor.from_pretrained("facebook/wav2vec2-large-xlsr-53", local_files_only=is_offline())
    
    stt_model = AutoModelForCTC.from_pretrained("facebook/mms-1b-all", local_files_only=is_offline())
    stt_processor = AutoProcessor.from_pretrained("facebook/mms-1b-all", local_files_only=is_offline())

    def _get_correct_text(self, ex_id: str, session: Optional[Session]) -> Optional[str]:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            exercise = exercise_service.get_by_id(ex_id, session=session)
            
            if not exercise:
                logger.warning(f"Exercise item not found: {ex_id}")
                return False
            
            if not exercise.exercise_type in ['translate', 'essay', 'organize', 'answering', 'fill-in-the-blank']:
                logger.warning(f"Exercise item {ex_id} is not a translation exercise")
                return False
            
            return exercise.answer
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to retrieve correct text for Exercise {ex_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def _get_correct_audio_path(self, ex_id: str, correct_audio_index: int, session: Optional[Session]) -> Optional[str]:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            exercise = exercise_service.get_by_id(ex_id, session=session)
            
            if not exercise:
                logger.warning(f"Exercise item not found: {ex_id}")
                return False
            
            if not exercise.exercise_type in ['speaking', 'conversation']:
                logger.warning(f"Exercise item {ex_id} is not a speaking exercise")
                return False
            
            if not exercise.audio_files:
                logger.warning(f"Exercise item {ex_id} has no audio files")
                return False
            
            from .media import MediaService
            media_service = MediaService()

            _, correct_speaking_path = media_service.get_file_path("/".join(exercise.audio_files[correct_audio_index].split("/")[2:]))

            return correct_speaking_path
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
        input_processed = self.stt_processor(waveform, sampling_rate=16000, return_tensors="pt", padding=True)
        logits = self.stt_model(**input_processed).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.stt_processor.batch_decode(predicted_ids)[0]
        return transcription

    def _compute_cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        return float(1-cosine(u = vec1, v = vec2))
    
    def _compute_grammar_error_rate(self, user_translation: str, correct_translation: str) -> float:
        language_code, _ = detect_text_language(correct_translation)
        tool = language_tool_python.LanguageTool(language_code)
        matches = tool.check(user_translation)
        num_errors = min(8, len(matches))
        return 1 - 1/(10-num_errors)  # Simple heuristic: more errors lead to lower score, but never below 0.5
    
    def _compute_token_differences_rate(self, user_translation: str, correct_translation: str) -> float:
        language_code, _ = detect_text_language(correct_translation)
        nlp = load_spacy_model(language_code)

        user_doc = nlp(user_translation)
        correct_doc = nlp(correct_translation)

        user_tokens = set(t.text.lower() for t in user_doc if not t.is_punct and not t.is_space)
        correct_tokens = set(t.text.lower() for t in correct_doc if not t.is_punct and not t.is_space)

        if not user_tokens:
            return 1.0 if not correct_tokens else 0.5  # If no tokens in user answer, score is 1 if correct also has none, otherwise 0.5

        common_tokens = correct_tokens.intersection(user_tokens)
        return min(1, len(common_tokens) / len(user_tokens))  # Proportion of correct tokens present in user's answer
    
    def _evaluate_text(self, ex_id: str, user_text: str) -> dict[str, float]:
        correct_text = self._get_correct_text(ex_id, session=None)
        if not correct_text:
            logger.warning(f"Could not retrieve correct text for Exercise {ex_id}. Returning score of 0.")
            raise ValueError("Correct text not found for the given exercise ID.")
        
        embedding_similarity = self._compute_cosine_similarity(
            self.text_embedding_model.encode(user_text),
            self.text_embedding_model.encode(correct_text)
        )
        grammar_error_rate = self._compute_grammar_error_rate(user_text, correct_text)
        token_difference_rate = self._compute_token_differences_rate(user_text, correct_text)

        return {
            "score": 0.6 * embedding_similarity + 0.25 * grammar_error_rate + 0.15 * token_difference_rate,
            "similarity": embedding_similarity,
            "grammar_error_rate": grammar_error_rate,
            "token_difference_rate": token_difference_rate
        }
    
    def _evaluate_speech(self, ex_id: str, user_audio_path: str, correct_audio_index: int) -> dict[str, float]:
        correct_audio_path = self._get_correct_audio_path(ex_id, correct_audio_index, session=None)
        if not correct_audio_path:
            logger.warning(f"Could not retrieve correct audio path for Exercise {ex_id}. Returning score of 0.")
            raise ValueError("Correct audio path not found for the given exercise ID.")

        correct_waveform = self._extract_waveform_from_path(correct_audio_path)
        user_waveform = self._extract_waveform_from_path(user_audio_path)
        
        embedding_similarity = self._compute_cosine_similarity(
            self._speech_to_embeddings(user_waveform),
            self._speech_to_embeddings(correct_waveform)
        )

        user_transcription = self._speech_to_text(user_waveform)
        correct_transcription = self._speech_to_text(correct_waveform)

        grammar_error_rate = self._compute_grammar_error_rate(
            user_transcription,
            correct_transcription
        )

        token_difference_rate = self._compute_token_differences_rate(
            user_transcription,
            correct_transcription
        )

        return {
            "score": 0.6 * embedding_similarity + 0.25 * grammar_error_rate + 0.15 * token_difference_rate,
            "similarity": embedding_similarity,
            "grammar_error_rate": grammar_error_rate,
            "token_difference_rate": token_difference_rate
        }

    def evaluate(self, ex_id: str, user_input: str, input_type: str, threshold: float = 0.8, correct_audio_index: int = 0) -> float:
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
        return {
            "correct": results["score"] > threshold,
            "score": results["score"],
            "feedback": "" ## TODO
        }