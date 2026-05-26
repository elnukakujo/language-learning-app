from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

import logging
logger = logging.getLogger(__name__)

from ...schemas.features import VocabularyDict
from ...schemas.data_collection.progress_tracking import ProgressTrackingDict
from ...models.features import Vocabulary
from ...models.system_data import Tag, Source
from ..containers import LessonService, LanguageService
from ..components import WordService, PassageService
from ..data_collection import ProgressTrackingService
from ...core.database import db_manager
from ...utils import update_score, update_difficulty

lesson_service = LessonService()
language_service = LanguageService()
word_service = WordService()
passage_service = PassageService()
progress_tracking_service = ProgressTrackingService()


class VocabularyService:
    def _serialize(self, vocabulary: Vocabulary | None, as_dict: bool, include_relations: bool) -> Vocabulary | dict | None:
        if not as_dict or vocabulary is None:
            return vocabulary
        return vocabulary.to_dict(include_relations=include_relations)

    def _serialize_list(self, vocabularies: list[Vocabulary], as_dict: bool, include_relations: bool) -> list[Vocabulary] | list[dict]:
        if not as_dict:
            return vocabularies
        return [vocabulary.to_dict(include_relations=include_relations) for vocabulary in vocabularies]

    def get_all(
        self,
        language_id: Optional[str] = None,
        lesson_id: Optional[str] = None,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> list[Vocabulary] | list[dict]:
        """
        Get all vocabulary for a specific language or lesson.

        Args:
            language_id (Optional[str]): The id of the language to get all the vocabulary from
            lesson_id (Optional[str]): The id of the lesson to get all the vocabulary from

        Returns:
            List of VocabularyFeature objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            assert not (language_id and lesson_id), f"language_id and lesson_id can't be both specified, but got: {language_id} and {lesson_id}"
            if language_id:
                lessons = lesson_service.get_all(language_id=language_id, session=session)

                vocabulary = []
                for lesson in lessons:
                    vocabulary.extend(
                        db_manager.find_all(
                            model_class=Vocabulary,
                            filters={'lesson_id': lesson.id},
                            session=session
                        )
                    )
                return self._serialize_list(vocabulary, as_dict, include_relations)
            elif lesson_id:
                vocabulary = db_manager.find_all(
                    model_class=Vocabulary,
                    filters={'lesson_id': lesson_id},
                    session=session
                )
                return self._serialize_list(vocabulary, as_dict, include_relations)
            else:
                raise ValueError(f"Requires either language_id or lesson_id but got: {language_id} and {lesson_id}")
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get all vocabularies: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(
        self,
        voc_id: str,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Vocabulary | dict | None:
        """
        Get a vocabulary item by its ID.

        Args:
            voc_id: The ID of the vocabulary item to retrieve.

        Returns:
            VocabularyFeature object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            vocabulary = db_manager.find_by_attr(
                model_class=Vocabulary,
                attr_values={'id': voc_id},
                session=session
            )
            return self._serialize(vocabulary, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get vocabulary by id: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_level(
        self,
        language_id: Optional[str],
        lesson_id: Optional[str],
        level: int,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> list[Vocabulary] | list[dict]:
        """
        Get all vocabulary items of a specific level among a language.
        
        Args:
            language_id: The id of the language to filter vocabulary items
            lesson_id: The id of the lesson to filter vocabulary items
            level: Vocabulary level (e.g., 0, 1, 2, etc.)
        
        Returns:
            List of matching VocabularyFeature objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            assert not (language_id and lesson_id), f"language_id and lesson_id can't be both specified, but got: {language_id} and {lesson_id}"

            if language_id:
                lessons = lesson_service.get_all(language_id=language_id, session=session)

                vocabulary = []
                for lesson in lessons:
                    vocabulary.extend(
                        db_manager.find_all(
                            model_class=Vocabulary,
                            filters={'lesson_id': lesson.id, 'level': level},
                            session=session
                        )
                    )
                return self._serialize_list(vocabulary, as_dict, include_relations)
            elif lesson_id:
                vocabulary = db_manager.find_all(
                    model_class=Vocabulary,
                    filters={'level': level, 'lesson_id': lesson_id},
                    session=session
                )
                return self._serialize_list(vocabulary, as_dict, include_relations)
            else:
                raise ValueError(f"Requires either language_id or lesson_id but got: {language_id} and {lesson_id}")
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get_by_level vocabularies: {e}")
            raise
        finally:
            if owns_session:
                session.close()
    
    def create(
        self,
        data: VocabularyDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Vocabulary | dict | None:
        """
        Create a new vocabulary item.

        Args:
            data: VocabularyDict containing vocabulary item details.

        Returns:
            Created VocabularyFeature object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            lesson = lesson_service.get_by_id(data.lesson_id, session=session)

            if not lesson:
                logger.warning(f"Cannot create vocabulary item, lesson not found: {data.lesson_id}")
                return None
            
            data.word.language_id = lesson.language_id
            word = word_service.create(data.word, session=session)
            if not word:
                logger.error(f"Failed to create word for vocabulary")
                return None

            # Create Passages using PassageService to ensure they're properly persisted
            example_sentences = []
            for example_sentence in (data.example_sentences or []):
                example_sentence.language_id = lesson.language_id
                passage = passage_service.create(example_sentence, session=session)
                if passage:
                    example_sentences.append(passage)

            # Create Vocabulary with references to the persisted Word and Passages
            vocabulary = Vocabulary(
                id=db_manager.generate_new_id(
                    model_class=Vocabulary,
                    session=session
                ),
                word_id=word.id,
                lesson_id=data.lesson_id,
                image_files=data.image_files or [],
                audio_files=data.audio_files or [],
                example_sentences=example_sentences,
                tags= session.query(Tag).filter(Tag.id.in_([t.id for t in data.tags])).all() if data.tags else [],
                sources= session.query(Source).filter(Source.id.in_([s.id for s in data.sources])).all() if data.sources else []
            )
                        
            result = db_manager.insert(
                obj=vocabulary,
                session=session
            )

            if result:
                logger.info(f"Created new VocabularyFeature item with ID: {result.id}")
            else:
                logger.error(f"Failed to create new VocabularyFeature item: {word.word}")

            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to create vocabulary: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update(
        self,
        voc_id: str,
        data: VocabularyDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Vocabulary | dict | None:
        """
        Update an existing VocabularyFeature item.

        Args:
            voc_id: The ID of the VocabularyFeature item to update.
            data: VocabularyDict containing updated vocabulary item details.

        Returns:
            Updated VocabularyFeature object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            existing = self.get_by_id(voc_id, session=session)
            
            if not existing:
                logger.warning(f"VocabularyFeature item not found: {voc_id}")
                return None
            
            if data.word is not None:
                data.word.language_id = existing.lesson.language_id
                word = word_service.create(data.word, session=session)
                if word:
                    existing.word = word
                    existing.word_id = word.id
            
            existing.example_sentences = []
            if data.example_sentences is not None:
                for example_sentence_data in data.example_sentences:
                    example_sentence_data.language_id = existing.lesson.language_id if existing.lesson else None
                    passage = passage_service.create(example_sentence_data, session=session)
                    if passage:
                        existing.example_sentences.append(passage)
            
            # Remove nested objects from update_data to avoid overwriting our service-managed updates
            update_data = data.model_dump(exclude={'id', 'lesson_id', 'score', 'difficulty', 'status', 'created_at', 'last_seen_at', 'word', 'word_id', 'example_sentences', 'tags', 'sources'}, exclude_none=True)
            
            # Update remaining fields
            for key, value in update_data.items():
                setattr(existing, key, value)
            
            # Save to database
            result = db_manager.modify(existing, session=session)
            
            if result:
                logger.info(f"Updated VocabularyFeature item: {voc_id}")
            else:
                logger.error(f"Failed to update VocabularyFeature item: {voc_id}")
            
            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update vocabulary: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def delete(self, voc_id: str, session: Optional[Session] = None) -> bool:
        """
        Delete a VocabularyFeature item by its ID.

        Args:
            voc_id: The ID of the VocabularyFeature item to delete.

        Returns:
            True if deletion was successful, else False
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            # Check if vocabulary item exists before deleting
            existing = self.get_by_id(voc_id, session=session)
            
            if not existing:
                logger.warning(f"VocabularyFeature item not found: {voc_id}")
                return False
            
            # Delete from database
            success = db_manager.delete(existing, session=session)
            
            if success:
                logger.info(f"Deleted VocabularyFeature item: {voc_id}")
            else:
                logger.error(f"Failed to delete VocabularyFeature item: {voc_id}")
            
            return success
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update vocabulary: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update_score(
        self,
        voc_id: str,
        score: float,
        duration_ms: float,
        hint_used: bool = False,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Vocabulary | dict | None:
        """
        Update VocabularyFeature item score based on average of all of its components scores.
        
        This should be called whenever a component's score changes.
        
        Args:
            voc_id: The ID of the VocabularyFeature item to update
            score: The new score for the VocabularyFeature item
        
        Returns:
            Updated VocabularyFeature object if successful, None otherwise
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            vocabulary = self.get_by_id(voc_id, session=session)
            
            if not vocabulary:
                logger.warning(f"VocabularyFeature item not found: {voc_id}")
                return None
            
            previous_score = vocabulary.score
            
            vocabulary.score = update_score(
                score=vocabulary.score,
                last_seen_at=vocabulary.last_seen_at,
                similarity=score
            )

            vocabulary.difficulty = update_difficulty(
                new_score=score,
                last_seen_at=vocabulary.last_seen_at,
                previous_difficulty=vocabulary.difficulty,
                created_at=vocabulary.created_at
            )

            # Update last_seen_at
            vocabulary.last_seen_at = datetime.now()
            
            # Save changes
            result = db_manager.modify(vocabulary, session=session)

            if result:
                logger.info(f"Updated VocabularyFeature {voc_id} score to {vocabulary.score} and difficulty to {vocabulary.difficulty}")

                progress_tracking_service.create(
                    data=ProgressTrackingDict(
                        user_id=vocabulary.lesson.user_id,
                        language_id=vocabulary.lesson.language_id,
                        element_id=voc_id,
                        element_type="vocabulary",
                        element_status=vocabulary.status,
                        score_before=previous_score,
                        score_after=result.score,
                        result=result.score >= previous_score, # Consider it a "success" (1) if the score improved or stayed the same
                        duration_ms=min(duration_ms, 10*60*1000), # Cap duration at 10 minutes to avoid skewing data with outliers
                        hint_used=hint_used,
                    ),
                    session=session,
                )

            if vocabulary.score != previous_score:
                lesson_service.update_score(vocabulary.lesson_id, session=session)
                logger.info(f"Updated lesson {vocabulary.lesson_id} score due to VocabularyFeature {voc_id}")

                word_service.update_score(vocabulary.word_id, session=session)
                logger.info(f"Updated word {vocabulary.word_id} score due to VocabularyFeature {voc_id}")

                if vocabulary.example_sentences:
                    for passage in vocabulary.example_sentences:
                        passage_service.update_score(passage.id, session=session)
                        logger.info(f"Updated passage {passage.id} score due to VocabularyFeature {voc_id}")
                    
            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update vocabulary: {e}")
            raise
        finally:
            if owns_session:
                session.close()
