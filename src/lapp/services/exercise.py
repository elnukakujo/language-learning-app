from datetime import date
from typing import Optional

import logging
logger = logging.getLogger(__name__)

from ..schemas.element_dict import ExerciseDict
from ..models import Exercise
from ..core.database import db_manager
from ..utils import update_score
from .unit import UnitService
from .character import CharacterService
from .vocabulary import VocabularyService
from .grammar import GrammarService

unit_service = UnitService()
character_service = CharacterService()
vocabulary_service = VocabularyService()
grammar_service = GrammarService()

class ExerciseService:
    def _check_associate_components(
        self, 
        character_ids: Optional[list[str]],
        vocabulary_ids: Optional[list[str]],
        grammar_ids: Optional[list[str]]
    ) -> tuple[list[str], list[str], list[str]]:
        """Validate and filter associated component IDs."""
        
        valid_char_ids = [
            cid for cid in (character_ids or [])
            if character_service.get_by_id(char_id=cid)
        ]
        
        valid_grammar_ids = [
            gid for gid in (grammar_ids or [])
            if grammar_service.get_by_id(grammar_id=gid)
        ]
        
        valid_voc_ids = [
            vid for vid in (vocabulary_ids or [])
            if vocabulary_service.get_by_id(voc_id=vid)
        ]
        
        return valid_char_ids, valid_voc_ids, valid_grammar_ids
    
    def _clean_exercise_associations(self, exercise: Exercise) -> bool:
        """
        Clean invalid association_ids from an exercise.
        
        Returns:
            True if any associations were cleaned, False otherwise
        """
        if not (exercise.character_ids or exercise.vocabulary_ids or exercise.grammar_ids):
            return False
        
        cleaned_char_ids, cleaned_voc_ids, cleaned_grammar_ids = self._check_associate_components(
            character_ids=exercise.character_ids,
            vocabulary_ids=exercise.vocabulary_ids,
            grammar_ids=exercise.grammar_ids
        )
        
        if (cleaned_char_ids != exercise.character_ids or
            cleaned_voc_ids != exercise.vocabulary_ids or
            cleaned_grammar_ids != exercise.grammar_ids):
            
            exercise.character_ids = cleaned_char_ids
            exercise.vocabulary_ids = cleaned_voc_ids
            exercise.grammar_ids = cleaned_grammar_ids
            db_manager.modify(exercise)
            return True
        
        return False
        
    def get_all(self, language_id: Optional[str] = None, unit_id: Optional[str] = None) -> list[Exercise]:
        """
        Get all exercises for a specific language or unit.

        Args:
            language_id (Optional[str] = None): The id of the language to get all the exercises from
            unit_id (Optional[str] = None): The id of the unit to get all the exercises from

        Returns:
            List of Exercise objects
        """
        assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"
        if language_id:
            exercises = db_manager.find_all(
                model_class=Exercise,
                filters={'language_id': language_id}
            )
        elif unit_id:
            exercises = db_manager.find_all(
                model_class=Exercise,
                filters={'unit_id': unit_id}
            )
        else:
            raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")
        
        if exercises:
            for ex in exercises:
                self._clean_exercise_associations(ex)
        return exercises

    def get_by_id(self, ex_id:str) -> Exercise | None:
        """
        Get a Exercise item by its ID.

        Args:
            ex_id: The ID of the Exercise item to retrieve.

        Returns:
            Exercise object if found, else None
        """
        exercise = db_manager.find_by_attr(
            model_class=Exercise,
            attr_values={'id': ex_id}
        )

        if exercise:
            self._clean_exercise_associations(exercise)
        return exercise

    def get_by_level(self, level: str, language_id: Optional[str] = None, unit_id: Optional[str] = None) -> list[Exercise]:
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
            exercises = db_manager.find_all(
                model_class=Exercise,
                filters={'level': level, 'unit_id': unit_id}
            )
        elif language_id:
            exercises = db_manager.find_all(
                model_class=Exercise,
                filters={'level': level, 'language_id': language_id}
            )
        else:
            exercises = db_manager.find_all(
                model_class=Exercise,
                filters={'level': level}
            )
        
        for ex in exercises:
            self._clean_exercise_associations(ex)
        return exercises
    
    def create(self, data: ExerciseDict) -> Exercise | None:
        """
        Create a new Exercise item.

        Args:
            data: ExerciseDict containing Exercise item details.

        Returns:
            Created Exercise object if successful, else None
        """
        unit = unit_service.get_by_id(data.unit_id)

        if not unit:
            logger.warning(f"Cannot create exercise item, unit not found: {data.unit_id}")
            return None
        
        if data.character_ids or data.vocabulary_ids or data.grammar_ids:
            data.character_ids, data.vocabulary_ids, data.grammar_ids = self._check_associate_components(
                character_ids=data.character_ids,
                vocabulary_ids=data.vocabulary_ids,
                grammar_ids=data.grammar_ids
            )

        exercise = Exercise(
            id = db_manager.generate_new_id(
                model_class=Exercise
            ),
            language_id = unit.language_id,
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
        
        if not unit_service.get_by_id(data.unit_id):
            logger.warning(f"Unit not found: {data.unit_id}, keeping existing unit_id: {existing.unit_id}")
            data.unit_id = existing.unit_id  # Revert to existing unit_id
        
        if data.character_ids or data.vocabulary_ids or data.grammar_ids:
            data.character_ids, data.vocabulary_ids, data.grammar_ids = self._check_associate_components(
                character_ids=data.character_ids,
                vocabulary_ids=data.vocabulary_ids,
                grammar_ids=data.grammar_ids
            )
        
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
        dependencies_lists = []
        if exercise.vocabulary_ids:
            for voc_id in exercise.vocabulary_ids:
                voc = vocabulary_service.get_by_id(voc_id=voc_id)
                if voc:
                    dependencies_lists.append(voc)
        if exercise.character_ids:
            for char_id in exercise.character_ids:
                char = character_service.get_by_id(char_id=char_id)
                if char:
                    dependencies_lists.append(char)
        if exercise.grammar_ids:
            for grammar_id in exercise.grammar_ids:
                grammar = grammar_service.get_by_id(grammar_id=grammar_id)
                if grammar:
                    dependencies_lists.append(grammar)

        for component in dependencies_lists:
            component.score = update_score(
                current_score=component.score,
                last_seen=component.last_seen,
                success=success
            )
            component.last_seen = date.today()

            db_manager.modify(component)
        
        return result