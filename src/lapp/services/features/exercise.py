from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

import logging
logger = logging.getLogger(__name__)

from ...schemas.features import ExerciseDict
from ...models.features import Exercise
from ...core.database import db_manager
from ...utils import update_score
from ..containers import UnitService
from .calligraphy import CalligraphyService
from .vocabulary import VocabularyService
from .grammar import GrammarService

unit_service = UnitService()
calligraphy_service = CalligraphyService()
vocabulary_service = VocabularyService()
grammar_service = GrammarService()

class ExerciseService:
    def _check_associate_components(
        self, 
        calligraphy_ids: Optional[list[str]],
        vocabulary_ids: Optional[list[str]],
        grammar_ids: Optional[list[str]],
        session: Optional[Session] = None
    ) -> tuple[list[str], list[str], list[str]]:
        """Validate and filter associated component IDs."""
        
        valid_calligraphy_ids = [
            cid for cid in (calligraphy_ids or [])
            if calligraphy_service.get_by_id(calligraphy_id=cid, session=session)
        ]
        
        valid_grammar_ids = [
            gid for gid in (grammar_ids or [])
            if grammar_service.get_by_id(grammar_id=gid, session=session)
        ]
        
        valid_voc_ids = [
            vid for vid in (vocabulary_ids or [])
            if vocabulary_service.get_by_id(voc_id=vid, session=session)
        ]
        
        return valid_calligraphy_ids, valid_voc_ids, valid_grammar_ids
    
    def _clean_exercise_associations(self, exercise: Exercise, session: Optional[Session] = None) -> bool:
        """
        Clean invalid association_ids from an exercise.
        
        Returns:
            True if any associations were cleaned, False otherwise
        """
        if not (exercise.calligraphy_ids or exercise.vocabulary_ids or exercise.grammar_ids):
            return False
        
        cleaned_calligraphy_ids, cleaned_voc_ids, cleaned_grammar_ids = self._check_associate_components(
            calligraphy_ids=exercise.calligraphy_ids,
            vocabulary_ids=exercise.vocabulary_ids,
            grammar_ids=exercise.grammar_ids,
            session=session
        )
        
        if (cleaned_calligraphy_ids != exercise.calligraphy_ids or
            cleaned_voc_ids != exercise.vocabulary_ids or
            cleaned_grammar_ids != exercise.grammar_ids):
            
            exercise.calligraphy_ids = cleaned_calligraphy_ids
            exercise.vocabulary_ids = cleaned_voc_ids
            exercise.grammar_ids = cleaned_grammar_ids
            db_manager.modify(exercise, session=session)
            return True
        
        return False
        
    def get_all(self, language_id: Optional[str] = None, unit_id: Optional[str] = None, session: Optional[Session] = None) -> list[Exercise]:
        """
        Get all exercises for a specific language or unit.

        Args:
            language_id (Optional[str] = None): The id of the language to get all the exercises from
            unit_id (Optional[str] = None): The id of the unit to get all the exercises from

        Returns:
            List of Exercise objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"
            if language_id:
                units = unit_service.get_all(language_id=language_id, session=session)

                exercises = []
                for unit in units:
                    exercises.extend(
                        db_manager.find_all(
                            model_class=Exercise,
                            filters={'unit_id': unit.id},
                            session=session
                        )
                    )
            elif unit_id:
                exercises = db_manager.find_all(
                    model_class=Exercise,
                    filters={'unit_id': unit_id},
                    session=session
                )
            else:
                raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")
            
            if exercises:
                for ex in exercises:
                    self._clean_exercise_associations(ex, session=session)
            return exercises
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get all exercises: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(self, ex_id: str, session: Optional[Session] = None) -> Exercise | None:
        """
        Get a Exercise item by its ID.

        Args:
            ex_id: The ID of the Exercise item to retrieve.

        Returns:
            Exercise object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            exercise = db_manager.find_by_attr(
                model_class=Exercise,
                attr_values={'id': ex_id},
                session=session
            )

            if exercise:
                self._clean_exercise_associations(exercise, session=session)
            return exercise
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get exercise by id: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_level(self, level: str, language_id: Optional[str] = None, unit_id: Optional[str] = None, session: Optional[Session] = None) -> list[Exercise]:
        """
        Get all Exercise items of a specific level among a language.
        
        Args:
            language_id: The id of the language to filter Exercise items
            unit_id: The id of the unit to filter Exercise items
            level: Exercise level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching Exercise objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"

            if language_id:
                units = unit_service.get_all(language_id=language_id, session=session)

                exercises = []
                for unit in units:
                    exercises.extend(
                        db_manager.find_all(
                            model_class=Exercise,
                            filters={'unit_id': unit.id},
                            session=session
                        )
                    )
            elif unit_id:
                exercises = db_manager.find_all(
                    model_class=Exercise,
                    filters={'level': level, 'unit_id': unit_id},
                    session=session
                )
            else:
                raise ValueError(f"Requires either language_id or unit_id but got neither: {language_id} and {unit_id}")
            
            for ex in exercises:
                self._clean_exercise_associations(ex, session=session)
            return exercises
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get_by_level exercises: {e}")
            raise
        finally:
            if owns_session:
                session.close()
    
    def create(self, data: ExerciseDict, session: Optional[Session] = None) -> Exercise | None:
        """
        Create a new Exercise item.

        Args:
            data: ExerciseDict containing Exercise item details.

        Returns:
            Created Exercise object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            unit = unit_service.get_by_id(data.unit_id, session=session)

            if not unit:
                logger.warning(f"Cannot create Exercise item, unit not found: {data.unit_id}")
                return None
            
            if data.calligraphy_ids or data.vocabulary_ids or data.grammar_ids:
                data.calligraphy_ids, data.vocabulary_ids, data.grammar_ids = self._check_associate_components(
                    calligraphy_ids=data.calligraphy_ids,
                    vocabulary_ids=data.vocabulary_ids,
                    grammar_ids=data.grammar_ids,
                    session=session
                )

            exercise = Exercise(
                id = db_manager.generate_new_id(
                    model_class=Exercise,
                    session=session
                ),
                **data.model_dump(exclude_none=True)
            )
            result = db_manager.insert(
                obj=exercise,
                session=session
            )

            if result:
                logger.info(f"Created new Exercise item with ID: {result.id}")
            else:
                logger.error(f"Failed to create new Exercise item: {exercise.id}")

            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to create exercise: {e}")
            raise
        finally:
            if owns_session:
                session.close()

        return result

    def update(self, ex_id: str, data: ExerciseDict, session: Optional[Session] = None) -> Exercise | None:
        """
        Update an existing Exercise item.

        Args:
            ex_id: The ID of the Exercise item to update.
            data: ExerciseDict containing updated Exercise item details.
        Returns:
            Updated Exercise object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            existing = self.get_by_id(ex_id, session=session)
            
            if not existing:
                logger.warning(f"Exercise item not found: {ex_id}")
                return None
            
            if not unit_service.get_by_id(data.unit_id, session=session):
                logger.warning(f"Unit not found: {data.unit_id}, keeping existing unit_id: {existing.unit_id}")
                data.unit_id = existing.unit_id  # Revert to existing unit_id
            
            if data.calligraphy_ids or data.vocabulary_ids or data.grammar_ids:
                data.calligraphy_ids, data.vocabulary_ids, data.grammar_ids = self._check_associate_components(
                    calligraphy_ids=data.calligraphy_ids,
                    vocabulary_ids=data.vocabulary_ids,
                    grammar_ids=data.grammar_ids,
                    session=session
                )
            
            # Only update fields that were provided (partial updates)
            update_data = data.model_dump(exclude_unset=True, exclude_none=True)
            
            # Update the existing object's attributes
            for key, value in update_data.items():
                setattr(existing, key, value)
            
            # Update last_seen
            existing.last_seen = date.today()
            
            # Save to database
            result = db_manager.modify(existing, session=session)
            
            if result:
                logger.info(f"Updated Exercise item: {ex_id}")
            else:
                logger.error(f"Failed to update Exercise item: {ex_id}")
            
            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update exercise: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def delete(self, ex_id: str, session: Optional[Session] = None) -> bool:
        """
        Delete an Exercise item by its ID.

        Args:
            ex_id: The ID of the Exercise item to delete.
        Returns:
            True if deletion was successful, else False
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            # Check if Exercise item exists before deleting
            existing = self.get_by_id(ex_id, session=session)
            
            if not existing:
                logger.warning(f"Exercise item not found: {ex_id}")
                return False
            
            # Delete from database
            success = db_manager.delete(existing, session=session)
            
            if success:
                logger.info(f"Deleted Exercise item: {ex_id}")
            else:
                logger.error(f"Failed to delete Exercise item: {ex_id}")
            
            return success
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to delete exercise: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update_score(self, ex_id: str, success: bool, session: Optional[Session] = None) -> Exercise | None:
        """
        Update Exercise item score based on average of all of its components scores.
        
        This should be called whenever a component's score changes.
        
        Args:
            ex_id: The ID of the Exercise item to update
            success: Whether the latest attempt was successful
        
        Returns:
            Updated Exercise object if successful, None otherwise
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            exercise = self.get_by_id(ex_id, session=session)
            
            if not exercise:
                logger.warning(f"Exercise item not found: {ex_id}")
                return None
            
            previous_score = exercise.score
            
            exercise.score = update_score(
                score=exercise.score,
                last_seen=exercise.last_seen,
                success=success
            )
            
            # Update last_seen
            exercise.last_seen = date.today()

            # Save changes
            result = db_manager.modify(exercise, session=session)

            if result:
                logger.info(f"Updated Exercise item {ex_id} score: {result.score}")

            # Update scores of associated components
            dependencies_lists = []
            if exercise.vocabulary_ids:
                for voc_id in exercise.vocabulary_ids:
                    voc = vocabulary_service.get_by_id(voc_id=voc_id, session=session)
                    if voc:
                        dependencies_lists.append(voc)
            if exercise.calligraphy_ids:
                for calligraphy_id in exercise.calligraphy_ids:
                    calligraphy = calligraphy_service.get_by_id(calligraphy_id=calligraphy_id, session=session)
                    if calligraphy:
                        dependencies_lists.append(calligraphy)
            if exercise.grammar_ids:
                for grammar_id in exercise.grammar_ids:
                    grammar = grammar_service.get_by_id(grammar_id=grammar_id, session=session)
                    if grammar:
                        dependencies_lists.append(grammar)

            for feature in dependencies_lists:
                feature.score = update_score(
                    score=feature.score,
                    last_seen=feature.last_seen,
                    success=success
                )
                feature.last_seen = date.today()

                db_manager.modify(feature, session=session)

            if exercise.score != previous_score:
                unit_service.update_score(exercise.unit_id, session=session)
                logger.info(f"Updated unit {exercise.unit_id} score due to Exercise {ex_id}")
            
            # Ensure all attributes are loaded before closing session
            if owns_session and result:
                session.refresh(result)
            
            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update Exercise score for {ex_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()
