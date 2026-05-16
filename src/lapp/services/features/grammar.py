from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

import logging
logger = logging.getLogger(__name__)

from ...schemas.features import GrammarDict
from ...models.features import Grammar
from ...models.system_data import Tag, Source
from ..containers import LessonService, LanguageService
from ..components import PassageService, WordService
from ...core.database import db_manager
from ...utils import update_score, update_difficulty

lesson_service = LessonService()
language_service = LanguageService()
word_service = WordService()
passage_service = PassageService()

class GrammarService:
    def _serialize(self, grammar: Grammar | None, as_dict: bool, include_relations: bool) -> Grammar | dict | None:
        if not as_dict or grammar is None:
            return grammar
        return grammar.to_dict(include_relations=include_relations)

    def _serialize_list(self, grammars: list[Grammar], as_dict: bool, include_relations: bool) -> list[Grammar] | list[dict]:
        if not as_dict:
            return grammars
        return [grammar.to_dict(include_relations=include_relations) for grammar in grammars]

    def get_all(
        self,
        language_id: Optional[str] = None,
        lesson_id: Optional[str] = None,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> list[Grammar] | list[dict]:
        """
        Get all Grammar items for a specific language or lesson.

        Args:
            language_id (Optional[str] = None): The id of the language to get all the grammars from
            lesson_id (Optional[str] = None): The id of the lesson to get all the grammars from

        Returns:
            List of Grammar objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            assert not (language_id and lesson_id), f"language_id and lesson_id can't be both specified, but got: {language_id} and {lesson_id}"
            if language_id:
                lessons = lesson_service.get_all(language_id=language_id, session=session)

                grammars = []
                for lesson in lessons:
                    grammars.extend(
                        db_manager.find_all(
                            model_class=Grammar,
                            filters={'lesson_id': lesson.id},
                            session=session
                        )
                    )
                return self._serialize_list(grammars, as_dict, include_relations)
            elif lesson_id:
                grammars = db_manager.find_all(
                    model_class=Grammar,
                    filters={'lesson_id': lesson_id},
                    session=session
                )
                return self._serialize_list(grammars, as_dict, include_relations)
            else:
                raise ValueError(f"Requires either language_id or lesson_id but got: {language_id} and {lesson_id}")
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get all grammars: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(
        self,
        grammar_id: str,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Grammar | dict | None:
        """
        Get a Grammar item by its ID.

        Args:
            grammar_id: The ID of the Grammar item to retrieve.

        Returns:
            Grammar object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            grammar = db_manager.find_by_attr(
                model_class=Grammar,
                attr_values={'id': grammar_id},
                session=session
            )
            return self._serialize(grammar, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get grammar by id: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_level(
        self,
        level: str,
        language_id: Optional[str] = None,
        lesson_id: Optional[str] = None,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> list[Grammar] | list[dict]:
        """
        Get all Grammar items of a specific level among a language.
        
        Args:
            language_id: The id of the language to filter Grammar items
            lesson_id: The id of the lesson to filter Grammar items
            level: Grammar level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching Grammar objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            assert not (language_id and lesson_id), f"language_id and lesson_id can't be both specified, but got: {language_id} and {lesson_id}"

            if language_id:
                lessons = lesson_service.get_all(language_id=language_id, session=session)

                grammars = []
                for lesson in lessons:
                    grammars.extend(
                        db_manager.find_all(
                            model_class=Grammar,
                            filters={'level': level, 'lesson_id': lesson.id},
                            session=session
                        )
                    )
                return self._serialize_list(grammars, as_dict, include_relations)
            elif lesson_id:
                grammars = db_manager.find_all(
                    model_class=Grammar,
                    filters={'level': level, 'lesson_id': lesson_id},
                    session=session
                )
                return self._serialize_list(grammars, as_dict, include_relations)
            else:
                raise ValueError(f"Requires either language_id or lesson_id but got: {language_id} and {lesson_id}")
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get_by_level grammars: {e}")
            raise
        finally:
            if owns_session:
                session.close()
    
    def create(
        self,
        data: GrammarDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Grammar | dict | None:
        """
        Create a new Grammar item.

        Args:
            data: GrammarDict containing Grammar item details.

        Returns:
            Created Grammar object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            lesson = lesson_service.get_by_id(data.lesson_id, session=session)

            if not lesson:
                logger.warning(f"Cannot create Grammar item, lesson not found: {data.lesson_id}")
                return None

            # Create Passages using PassageService
            example_sentences = []
            for sentence in (data.example_sentences or []):
                sentence.language_id = lesson.language_id
                passage = passage_service.create(sentence, session=session)
                if passage:
                    example_sentences.append(passage)

            grammar = Grammar(
                id = db_manager.generate_new_id(
                    model_class=Grammar,
                    session=session
                ),
                lesson_id=lesson.id,
                title=data.title,
                explanation=data.explanation,
                example_sentences=example_sentences,
                tags= session.query(Tag).filter(Tag.id.in_([t.id for t in data.tags])).all() if data.tags else [],
                sources= session.query(Source).filter(Source.id.in_([s.id for s in data.sources])).all() if data.sources else []
            )
                        
            result = db_manager.insert(
                obj=grammar,
                session=session
            )

            if result:
                logger.info(f"Created new Grammar item with ID: {result.id}")
            else:
                logger.error(f"Failed to create new Grammar item: {grammar.title}")

            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to create grammar: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update(
        self,
        grammar_id: str,
        data: GrammarDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Grammar | dict | None:
        """
        Update an existing Grammar item.

        Args:
            grammar_id: The ID of the Grammar item to update.
            data: GrammarDict containing updated Grammar item details.

        Returns:
            Updated Grammar object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            existing = self.get_by_id(grammar_id, session=session)
            
            if not existing:
                logger.warning(f"Grammar item not found: {grammar_id}")
                return None
            
            existing.example_words = []
            if data.example_words is not None:
                for example_word_data in data.example_words:
                    example_word_data.language_id = existing.lesson.language_id
                    word = word_service.create(example_word_data, session=session)
                    if word:
                        existing.example_words.append(word)
                
            
            # Handle example_sentences update through PassageService if provided
            existing.example_sentences = []
            if data.example_sentences is not None:
                for sentence in data.example_sentences:
                    sentence.language_id = existing.lesson.language_id
                    passage = passage_service.create(sentence, session=session)
                    if passage:
                        existing.example_sentences.append(passage)
                            
            # Remove nested objects from update_data
            update_data = data.model_dump(exclude={'id', 'lesson_id', 'score', 'difficulty', 'status', 'created_at', 'last_seen_at', 'example_words', 'example_sentences', 'tags', 'sources'}, exclude_none=True)
            
            # Update the existing object's attributes
            for key, value in update_data.items():
                setattr(existing, key, value)
            
            # Save to database
            result = db_manager.modify(existing, session=session)
            
            if result:
                logger.info(f"Updated Grammar item: {grammar_id}")
            else:
                logger.error(f"Failed to update Grammar item: {grammar_id}")
            
            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update grammar: {e}", exc_info=True)
            raise
        finally:
            if owns_session:
                session.close()

    def delete(self, grammar_id: str, session: Optional[Session] = None) -> bool:
        """
        Delete a Grammar item by its ID.

        Args:
            grammar_id: The ID of the Grammar item to delete.
        Returns:
            True if deletion was successful, else False
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            # Check if grammar item exists before deleting
            existing = self.get_by_id(grammar_id, session=session)
            
            if not existing:
                logger.warning(f"Grammar item not found: {grammar_id}")
                return False
            
            # Delete from database
            success = db_manager.delete(existing, session=session)
            
            if success:
                logger.info(f"Deleted Grammar item: {grammar_id}")
            else:
                logger.error(f"Failed to delete Grammar item: {grammar_id}")
            
            return success
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to delete grammar: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update_score(
        self,
        grammar_id: str,
        score: float,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Grammar | dict | None:
        """
        Update Grammar item score based on average of all of its components scores.
        
        This should be called whenever a component's score changes.
        
        Args:
            grammar_id: The ID of the Grammar item to update
            score: The new score for the Grammar item
        
        Returns:
            Updated Grammar object if successful, None otherwise
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            grammar = self.get_by_id(grammar_id, session=session)
        
            if not grammar:
                logger.warning(f"Grammar item not found: {grammar_id}")
                return None
            
            previous_score = grammar.score

            grammar.score = update_score(
                score=grammar.score,
                last_seen_at=grammar.last_seen_at,
                similarity=score
            )

            grammar.difficulty = update_difficulty(
                new_score=score,
                last_seen_at=grammar.last_seen_at,
                previous_difficulty=grammar.difficulty,
                created_at=grammar.created_at
            )
            
            # Update last_seen_at
            grammar.last_seen_at = datetime.now()

            # Save changes
            result = db_manager.modify(grammar, session=session)
            
            if result:
                logger.info(f"Updated GrammarFeature {grammar_id} score to {grammar.score} and difficulty to {grammar.difficulty}")

            if grammar.score != previous_score:
                lesson_service.update_score(grammar.lesson_id, session=session)
                logger.info(f"Updated lesson {grammar.lesson_id} score due to Grammar {grammar_id}")

                if grammar.example_words:
                    for word in grammar.example_words:
                        word_service.update_score(word.id, session=session)
                        logger.info(f"Updated example Word {word.id} score due to Grammar {grammar_id}")

                if grammar.example_sentences:
                    for passage in grammar.example_sentences:
                        passage_service.update_score(passage.id, session=session)
                        logger.info(f"Updated example Passage {passage.id} score due to Grammar {grammar_id}")
            
            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update grammar score: {e}")
            raise
        finally:
            if owns_session:
                session.close()
