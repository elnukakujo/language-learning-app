from datetime import date
from typing import Optional

import logging
logger = logging.getLogger(__name__)

from ..schemas.element_dict import VocabularyDict
from ..models import Vocabulary
from ..core.database import db_manager
from ..utils import update_score

class VocabularyService:
    def get_all(self, language_id: Optional[str], unit_id: Optional[str]) -> list[Vocabulary]:
        """
        Get all vocabulary for a specific language or unit.

        Args:
            language_id (Optional[str]): The id of the language to get all the vocabulary from
            unit_id (Optional[str]): The id of the unit to get all the vocabulary from

        Returns:
            List of Vocabulary objects
        """
        assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"
        if language_id:
            return db_manager.find_all(
                model_class=Vocabulary,
                filters={'language_id': language_id}
            )
        elif unit_id:
            return db_manager.find_all(
                model_class=Vocabulary,
                filters={'unit_id': unit_id}
            )
        else:
            raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")

    def get_by_id(self, voc_id:str) -> Vocabulary | None:
        """
        Get a vocabulary item by its ID.

        Args:
            voc_id: The ID of the vocabulary item to retrieve.

        Returns:
            Vocabulary object if found, else None
        """
        return db_manager.find_by_attr(
            model_class=Vocabulary,
            attr_values={'id': voc_id}
        )

    def get_by_level(self, language_id: Optional[str], unit_id: Optional[str], level: str) -> list[Vocabulary]:
        """
        Get all vocabulary items of a specific level among a language.
        
        Args:
            language_id: The id of the language to filter vocabulary items
            unit_id: The id of the unit to filter vocabulary items
            level: Vocabulary level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching Vocabulary objects
        """
        assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"

        if unit_id:
            return db_manager.find_all(
                model_class=Vocabulary,
                filters={'level': level, 'unit_id': unit_id}
            )
        elif language_id:
            return db_manager.find_all(
                model_class=Vocabulary,
                filters={'level': level, 'language_id': language_id}
            )
        else:
            raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")
    
    def create(self, data: VocabularyDict) -> Vocabulary | None:
        """
        Create a new vocabulary item.

        Args:
            data: VocabularyDict containing vocabulary item details.

        Returns:
            Created Vocabulary object if successful, else None
        """
        vocabulary = Vocabulary(
            **data.model_dump(exclude_none=True)
        )
        result = db_manager.insert(
            obj=vocabulary
        )

        if result:
            logger.info(f"Created new vocabulary item with ID: {result.id}")
        else:
            logger.error(f"Failed to create new vocabulary item: {vocabulary.word}")

        return result

    def update(self, voc_id: str, data: VocabularyDict) -> Vocabulary | None:
        """
        Update an existing vocabulary item.

        Args:
            voc_id: The ID of the vocabulary item to update.
            data: VocabularyDict containing updated vocabulary item details.

        Returns:
            Updated Vocabulary object if successful, else None
        """
        existing = self.get_by_id(voc_id)
        
        if not existing:
            logger.warning(f"Vocabulary item not found: {voc_id}")
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
            logger.info(f"Updated vocabulary item: {voc_id}")
        else:
            logger.error(f"Failed to update vocabulary item: {voc_id}")
        
        return result

    def delete(self, voc_id: str) -> bool:
        """
        Delete a vocabulary item by its ID.

        Args:
            voc_id: The ID of the vocabulary item to delete.

        Returns:
            True if deletion was successful, else False
        """
        # Check if vocabulary item exists before deleting
        existing = self.get_by_id(voc_id)
        
        if not existing:
            logger.warning(f"Vocabulary item not found: {voc_id}")
            return False
        
        # Delete from database
        success = db_manager.delete(existing)
        
        if success:
            logger.info(f"Deleted vocabulary item: {voc_id}")
        else:
            logger.error(f"Failed to delete vocabulary item: {voc_id}")
        
        return success

    def update_score(self, voc_id: str, success: bool) -> Vocabulary | None:
        """
        Update vocabulary item score based on average of all of its components scores.
        
        This should be called whenever a component's score changes.
        
        Args:
            voc_id: The ID of the vocabulary item to update
            success: Whether the latest attempt was successful
        
        Returns:
            Updated Vocabulary object if successful, None otherwise
        """
        vocabulary = self.get_by_id(voc_id)
        
        if not vocabulary:
            logger.warning(f"Vocabulary item not found: {voc_id}")
            return None
        
        vocabulary.score = update_score(
            current_score=vocabulary.score,
            last_seen=vocabulary.last_seen,
            success=success
        )
        
        # Update last_seen
        vocabulary.last_seen = date.today()
        
        # Save changes
        result = db_manager.modify(vocabulary)
        
        if result:
            logger.info(f"Updated vocabulary item {voc_id} score: {result.score}")
        
        return result