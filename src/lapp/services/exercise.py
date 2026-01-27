from datetime import date
from typing import Optional

import logging

logger = logging.getLogger(__name__)

from ..schemas.element_dict import ExerciseDict
from ..models import Exercise
from ..core.database import db_manager
from ..utils import update_score

class ExerciseService:
    def get_all(self, language_id: Optional[str], unit_id: Optional[str]) -> list[Exercise]:
        """
        Get all exercises for a specific language or unit.

        Args:
            language_id (Optional[str]): The id of the language to get all the exercises from
            unit_id (Optional[str]): The id of the unit to get all the exercises from

        Returns:
            List of Exercise objects
        """
        assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"
        if language_id:
            return db_manager.find_all(
                model_class=Exercise,
                filters={'language_id': language_id}
            )
        elif unit_id:
            return db_manager.find_all(
                model_class=Exercise,
                filters={'unit_id': unit_id}
            )
        else:
            raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")

    def get_by_id(self, ex_id:str) -> Exercise | None:
        """
        Get a Exercise item by its ID.

        Args:
            ex_id: The ID of the Exercise item to retrieve.

        Returns:
            Exercise object if found, else None
        """
        return db_manager.find_by_attr(
            model_class=Exercise,
            attr_values={'id': ex_id}
        )

    def get_by_level(self, language_id: Optional[str], unit_id: Optional[str], level: str) -> list[Exercise]:
        """
        Get all Exercise items of a specific level among a language.
        
        Args:
            language_id: The id of the language to filter Exercise items
            unit_id: The id of the unit to filter Exercise items
            level: Exercise level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching Exercise objects
        """
        assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"

        if unit_id:
            return db_manager.find_all(
                model_class=Exercise,
                filters={'level': level, 'unit_id': unit_id}
            )
        elif language_id:
            return db_manager.find_all(
                model_class=Exercise,
                filters={'level': level, 'language_id': language_id}
            )
        else:
            raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")
    
    def create(self, data: ExerciseDict) -> Exercise | None:
        """
        Create a new Exercise item.

        Args:
            data: ExerciseDict containing Exercise item details.

        Returns:
            Created Exercise object if successful, else None
        """
        exercise = Exercise(
            **data.model_dump(exclude_none=True)
        )
        result = db_manager.insert(
            obj=exercise
        )

        if result:
            logger.info(f"Created new exercise item with ID: {result.id}")
        else:
            logger.error(f"Failed to create new exercise item: {exercise.id}")

        return result

    def update(self, ex_id: str, data: ExerciseDict) -> Exercise | None:
        """
        Update an existing Exercise item.

        Args:
            ex_id: The ID of the Exercise item to update.
            data: ExerciseDict containing updated Exercise item details.
        Returns:
            Updated Exercise object if successful, else None
        """
        existing = self.get_by_id(ex_id)
        
        if not existing:
            logger.warning(f"Exercise item not found: {ex_id}")
            return None
        
        # Only update fields that were provided (partial updates)
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        
        # Update the existing object's attributes
        for key, value in update_data.items():
            setattr(existing, key, value)
        
        # Update last_seen
        existing.last_seen = date.today()
        
        # Save to database
        result = db_manager.modify(existing)
        
        if result:
            logger.info(f"Updated Exercise item: {ex_id}")
        else:
            logger.error(f"Failed to update Exercise item: {ex_id}")
        
        return result

    def delete(self, ex_id: str) -> bool:
        """
        Delete an Exercise item by its ID.

        Args:
            ex_id: The ID of the Exercise item to delete.

        Returns:
            True if deletion was successful, else False
        """
        # Check if Exercise item exists before deleting
        existing = self.get_by_id(ex_id)
        
        if not existing:
            logger.warning(f"Exercise item not found: {ex_id}")
            return False
        
        # Delete from database
        success = db_manager.delete(existing)
        
        if success:
            logger.info(f"Deleted Exercise item: {ex_id}")
        else:
            logger.error(f"Failed to delete Exercise item: {ex_id}")
        
        return success

    def update_score(self, ex_id: str, success: bool) -> Exercise | None:
        """
        Update Exercise item score based on average of all of its components scores.
        
        This should be called whenever a component's score changes.
        
        Args:
            ex_id: The ID of the Exercise item to update
            success: Whether the latest attempt was successful
        
        Returns:
            Updated Exercise object if successful, None otherwise
        """
        exercise = self.get_by_id(ex_id)
        
        if not exercise:
            logger.warning(f"Exercise item not found: {ex_id}")
            return None
        
        exercise.score = update_score(
            current_score=exercise.score,
            last_seen=exercise.last_seen,
            success=success
        )
        
        # Update last_seen
        exercise.last_seen = date.today()

        # Save changes
        result = db_manager.modify(exercise)

        if result:
            logger.info(f"Updated exercise item {ex_id} score: {result.score}")

        # Update scores of associated components
        dependencies_lists = (
            exercise.associated_vocs + 
            exercise.associated_characters + 
            exercise.associated_grammars
        )

        for component in dependencies_lists:
            component.score = update_score(
                current_score=component.score,
                last_seen=component.last_seen,
                success=success
            )
            component.last_seen = date.today()

            db_manager.modify(component)
        
        return result