from sentence_transformers import SentenceTransformer
from transformers import AutoProcessor, AutoModelForCTC
from scipy.spatial.distance import cosine
from sqlalchemy.orm import Session
from typing import Optional
import torchaudio
from ..utils import is_offline

import logging
logger = logging.getLogger(__name__)

from ..core.database import db_manager
from ..utils import detect_text_language, load_spacy_model
from .features import ExerciseService

exercise_service = ExerciseService()

class EvaluatorService:
    text_embedding_model = SentenceTransformer('all-MiniLM-L6-v2', local_files_only=is_offline())
    audio_embedding_model = AutoModelForCTC.from_pretrained("facebook/mms-1b-all", local_files_only=is_offline())
    audio_embedding_processor = AutoProcessor.from_pretrained("facebook/mms-1b-all", local_files_only=is_offline())

    def evaluate_translation(
        self,
        ex_id: str,
        user_translation: str,
        threshold: float = 0.8,
        session: Optional[Session] = None
    ) -> dict[str, any]:
        """
        Evaluate user's translation answer for an Exercise item.
        
        Args:
            ex_id: The ID of the Exercise item to evaluate
            user_translation: The user's translation answer to evaluate
        Returns:
            True if the translation is correct, False otherwise
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            exercise = exercise_service.get_by_id(ex_id, session=session)
            
            if not exercise:
                logger.warning(f"Exercise item not found: {ex_id}")
                return False
            
            if not exercise.exercise_type == 'translate':
                logger.warning(f"Exercise item {ex_id} is not a translation exercise")
                return False
            
            correct_translation = exercise.answer
            logger.info(f"Evaluating translation for Exercise {ex_id}. User answer: '{user_translation}', Correct answer: '{correct_translation}'")

            # Use sentence transformer to evaluate similarity
            embeddings = self.text_embedding_model.encode([user_translation, correct_translation])

            similarity = float(1-cosine(u = embeddings[0], v = embeddings[1]))
            logger.info(f"Calculated similarity for Exercise {ex_id}: {similarity}")

            language_code, _ = detect_text_language(correct_translation)
            logger.info(f"Detected language: {language_code}")

            tokens = []
            try:
                nlp = load_spacy_model(language_code)

                user_doc = nlp(user_translation)
                correct_doc = nlp(correct_translation)

                user_tokens = [t for t in user_doc if not t.is_punct and not t.is_space]
                correct_tokens = [t for t in correct_doc if not t.is_punct and not t.is_space]

                for u_tok in user_tokens:
                    best_sim = -1.0
                    best_idx: int | None = None

                    for i, c_tok in enumerate(correct_tokens):
                        if u_tok.text.lower() == c_tok.text.lower():
                            best_sim = 1.0
                            best_idx = i
                            break

                        if u_tok.has_vector and c_tok.has_vector:
                            sim = u_tok.similarity(c_tok)
                            if sim > best_sim:
                                best_sim = sim
                                best_idx = i

                    if best_sim >= 0.95:
                        tokens.append(
                            {
                                "word": u_tok.text,
                                "status": "correct"
                            }
                        )
                    elif best_sim >= 0.5:
                        tokens.append(
                            {
                                "word": u_tok.text,
                                "status": "close",
                                "expected": correct_tokens[best_idx].text if best_idx is not None else None
                            }
                        )
                    else:
                        tokens.append(
                            {
                                "word": u_tok.text,
                                "status": "wrong"
                            }
                        )

            except Exception as e:
                logger.warning(f"Failed to tokenize translation for Exercise {ex_id}: {e}")

            if similarity > threshold:
                correct = True
            else:
                correct = False

            return {
                "score": similarity,
                "correct": correct,
                "tokens": tokens,
            }
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to evaluate translation for Exercise {ex_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()
    
    def evaluate_speech(
            self, 
            ex_id: str, 
            user_audio_url: str,
            correct_audio_index: Optional[int] = 0,
            threshold: float = 0.8,
            session: Optional[Session] = None
        ) -> dict[str, any]:
        """
        Evaluate user's pronunciation answer for an Exercise item.
        
        Args:
            ex_id: The ID of the Exercise item to evaluate
            user_audio_url: The URL of the user's audio answer to evaluate
            correct_audio_index: The index of the correct audio file to compare against (default is 0)
            threshold: The similarity threshold for determining correct pronunciations
        
        Returns:
            A dictionary containing the evaluation results, including a score and feedback.
        """

        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            exercise = exercise_service.get_by_id(ex_id, session=session)
            
            if not exercise:
                logger.warning(f"Exercise item not found: {ex_id}")
                return {"score": 0.0, "correct": False, "feedback": "Exercise not found"}
            
            if not exercise.exercise_type in ['speaking', 'conversation']:
                logger.warning(f"Exercise item {ex_id} is not a speaking exercise")
                return {"score": 0.0, "correct": False, "feedback": "Exercise is not a speaking exercise"}
            
            if not exercise.audio_files:
                logger.warning(f"Exercise item {ex_id} has no audio files")
                return {"score": 0.0, "correct": False, "feedback": "Exercise has no audio files"}
            
            from .media import MediaService
            media_service = MediaService()

            _, correct_speaking_path = media_service.get_file_path("/".join(exercise.audio_files[correct_audio_index].split("/")[2:]))
            _, user_speaking_path = media_service.get_file_path(user_audio_url)

            # Load and preprocess audio files
            correct_waveform, correct_sr = torchaudio.load(correct_speaking_path)

            if correct_sr != 16000:
                correct_waveform = torchaudio.transforms.Resample(orig_freq=correct_sr, new_freq=16000)(correct_waveform)

            correct_waveform = correct_waveform.mean(dim=0).numpy()

            user_waveform, user_sr = torchaudio.load(user_speaking_path)

            if user_sr != 16000:
                user_waveform = torchaudio.transforms.Resample(orig_freq=user_sr, new_freq=16000)(user_waveform)

            user_waveform = user_waveform.mean(dim=0).numpy()
            
            # Get audio embeddings
            correct_inputs = self.audio_embedding_processor(correct_waveform, sampling_rate=16000, return_tensors="pt", padding=True)
            user_inputs = self.audio_embedding_processor(user_waveform, sampling_rate=16000, return_tensors="pt", padding=True)

            correct_outputs = self.audio_embedding_model(**correct_inputs, output_hidden_states=True)
            user_outputs = self.audio_embedding_model(**user_inputs, output_hidden_states=True)

            correct_embeddings = correct_outputs.hidden_states[-1].squeeze(0).mean(dim=0).detach().numpy()
            user_embeddings = user_outputs.hidden_states[-1].squeeze(0).mean(dim=0).detach().numpy()

            similarity = float(1-cosine(u = user_embeddings, v = correct_embeddings))
            logger.info(f"Calculated audio similarity for Exercise {ex_id}: {similarity}")

            correct = True if similarity > threshold else False

            return {
                "score": similarity,
                "correct": correct
            }

        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to evaluate speaking for Exercise {ex_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()