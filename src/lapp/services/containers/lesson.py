from datetime import datetime
from typing import Optional
import logging

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

from ...schemas.containers import LessonDict
from ...models.containers import Lesson
from ...models.system_data import Tag, Source
from ...models.features import Calligraphy, Vocabulary, Grammar, Exercise
from ...core.database import db_manager
from .language import LanguageService

language_service = LanguageService()

class LessonService:
    def _serialize(self, lesson: Lesson | None, as_dict: bool, include_relations: bool) -> Lesson | dict | None:
        if not as_dict or lesson is None:
            return lesson
        return lesson.to_dict(include_relations=include_relations)

    def _serialize_list(self, lessons: list[Lesson], as_dict: bool, include_relations: bool) -> list[Lesson] | list[dict]:
        if not as_dict:
            return lessons
        return [lesson.to_dict(include_relations=include_relations) for lesson in lessons]

    def get_all(
        self,
        language_id: str,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> list[Lesson] | list[dict]:
        """
        Get all lessons for a specific language.

        Args:
            language_id (str): The id of the language to get all the lessons from

        Returns:
            List of LessonContainer objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            lessons = db_manager.find_all(
                model_class=Lesson,
                filters={'language_id': language_id},
                session=session
            )
            return self._serialize_list(lessons, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get all lessons for language {language_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(
        self,
        lesson_id: str,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Lesson | dict | None:
        """
        Get a lesson by its ID.

        Args:
            lesson_id: The ID of the lesson to retrieve.

        Returns:
            LessonContainer object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            lesson = db_manager.find_by_attr(
                model_class=Lesson,
                attr_values={'id': lesson_id},
                session=session
            )
            return self._serialize(lesson, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get lesson {lesson_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_level(
        self,
        level: str,
        language_id: Optional[str] = None,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> list[Lesson] | list[dict]:
        """
        Get all lessons of a specific level among a language.
        
        Args:
            language_id: The id of the language to filter lessons
            level: Lesson level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching LessonContainer objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            if language_id:
                lessons = db_manager.find_all(
                    model_class=Lesson,
                    filters={'level': level, 'language_id': language_id},
                    session=session
                )
                return self._serialize_list(lessons, as_dict, include_relations)
            else:
                lessons = db_manager.find_all(
                    model_class=Lesson,
                    filters={'level': level},
                    session=session
                )
                return self._serialize_list(lessons, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get lessons by level {level}: {e}")
            raise
        finally:
            if owns_session:
                session.close()
    
    def create(
        self,
        data: LessonDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Lesson | dict | None:
        """
        Create a new lesson.

        Args:
            data: LessonDict containing lesson details.

        Returns:
            Created LessonContainer object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            lesson = Lesson(
                id = db_manager.generate_new_id(
                    model_class=Lesson,
                    session=session
                ),
                **{k: v for k, v in data.model_dump(exclude={'status', 'score', 'created_at', 'last_seen_at'}, exclude_none=True).items()},
                tags = session.query(Tag).filter(Tag.id.in_([t.id for t in data.tags])).all() if data.tags else [],
                sources = session.query(Source).filter(Source.id.in_([s.id for s in data.sources])).all() if data.sources else []
            )
            result = db_manager.insert(
                obj=lesson,
                session=session
            )

            if result:
                logger.info(f"Created new lesson with ID: {result.id}")
            else:
                logger.error(f"Failed to create new lesson: {lesson.title}")

            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to create lesson: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update(
        self,
        lesson_id: str,
        data: LessonDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Lesson | dict | None:
        """
        Update an existing lesson.

        Args:
            lesson_id: The ID of the lesson to update.
            data: LessonDict containing updated lesson details.

        Returns:
            Updated LessonContainer object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            existing = self.get_by_id(lesson_id, session=session)
            
            if not existing:
                logger.warning(f"LessonContainer not found: {lesson_id}")
                return None
            
            # Update the existing object's attributes
            update_data = data.model_dump(exclude={'id', 'language_id', 'score', 'status', 'created_at', 'last_seen_at'}, exclude_none=True)

            for key, value in update_data.items():
                setattr(existing, key, value)
            
            # Save to database
            result = db_manager.modify(existing, session=session)
            
            if result:
                logger.info(f"Updated lesson: {lesson_id}")
            else:
                logger.error(f"Failed to update lesson: {lesson_id}")
            
            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update lesson {lesson_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def delete(self, lesson_id: str, session: Optional[Session] = None) -> bool:
        """
        Delete a lesson by its ID.

        Args:
            lesson_id: The ID of the lesson to delete.

        Returns:
            True if deletion was successful, else False
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            # Check if lesson exists before deleting
            existing = self.get_by_id(lesson_id, session=session)
            
            if not existing:
                logger.warning(f"Lesson not found: {lesson_id}")
                return False
            
            # Delete from database
            success = db_manager.delete(existing, session=session)
            
            if success:
                logger.info(f"Deleted lesson: {lesson_id}")
            else:
                logger.error(f"Failed to delete lesson: {lesson_id}")
            
            return success
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to delete lesson {lesson_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update_score(self, lesson_id: str, session: Optional[Session] = None) -> Lesson | None:
        """
        Update lesson score based on average of all of its components scores.
        
        This should be called whenever a component's score changes.
        
        Args:
            lesson_id: The ID of the lesson to update
        
        Returns:
            Updated LessonContainer object if successful, None otherwise
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            lesson = self.get_by_id(lesson_id, session=session)
            
            if not lesson:
                logger.warning(f"LessonContainer not found: {lesson_id}")
                return None
            
            # Get all components for this language
            components = db_manager.find_all(
                model_class=[Vocabulary, Grammar, Calligraphy, Exercise],
                filters={'lesson_id': lesson_id},
                session=session
            )

            if not components:
                logger.warning(f"No components found for lesson: {lesson_id}")
                lesson.score = 0.0
            else:
                # Calculate average score from all lessons
                total_score = sum(component.score for component in components)
                lesson.score = round(total_score / len(components), 2)
                
                logger.info(
                    f"Calculated lesson score: {lesson.score} "
                    f"(from {len(components)} components)"
                )
            
            # Update last_seen
            lesson.last_seen_at = datetime.now()

            # Save changes
            result = db_manager.modify(lesson, session=session)
            if result:
                logger.info(f"Updated lesson {lesson_id} score: {result.score}")

            if not (language_service.update_score(lesson.language_id, session=session)):
                raise Exception(f"Failed to update language score for language {lesson.language_id} after lesson {lesson_id} score update.")
            
            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update lesson score for {lesson_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()
