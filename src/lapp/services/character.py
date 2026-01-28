from datetime import date
from typing import Optional

import logging


logger = logging.getLogger(__name__)

from ..schemas.element_dict import CharacterDict
from ..models import Character
from ..core.database import db_manager
from . import UnitService, LanguageService
from ..utils import update_score

unit_service = UnitService()
language_service = LanguageService()

class CharacterService:
    def get_all(self, language_id: Optional[str], unit_id: Optional[str]) -> list[Character]:
        """
        Get all characters for a specific language or unit.

        Args:
            language_id (Optional[str]): The id of the language to get all the characters from
            unit_id (Optional[str]): The id of the unit to get all the characters from

        Returns:
            List of Character objects
        """
        assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"
        if language_id:
            return db_manager.find_all(
                model_class=Character,
                filters={'language_id': language_id}
            )
        elif unit_id:
            return db_manager.find_all(
                model_class=Character,
                filters={'unit_id': unit_id}
            )
        else:
            raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")

    def get_by_id(self, char_id:str) -> Character | None:
        """
        Get a character item by its ID.

        Args:
            char_id: The ID of the character item to retrieve.

        Returns:
            Character object if found, else None
        """
        return db_manager.find_by_attr(
            model_class=Character,
            attr_values={'id': char_id}
        )

    def get_by_level(self, language_id: Optional[str], unit_id: Optional[str], level: str) -> list[Character]:
        """
        Get all character items of a specific level among a language.
        
        Args:
            language_id: The id of the language to filter character items
            unit_id: The id of the unit to filter character items
            level: Character level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching Character objects
        """
        assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"

        if unit_id:
            return db_manager.find_all(
                model_class=Character,
                filters={'level': level, 'unit_id': unit_id}
            )
        elif language_id:
            return db_manager.find_all(
                model_class=Character,
                filters={'level': level, 'language_id': language_id}
            )
        else:
            raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")
    
    def create(self, data: CharacterDict) -> Character | None:
        """
        Create a new character item.

        Args:
            data: CharacterDict containing character item details.

        Returns:
            Created Character object if successful, else None
        """
        unit = unit_service.get_by_id(data.unit_id)

        if not unit:
            logger.warning(f"Cannot create character item, unit not found: {data.unit_id}")
            return None
        
        character = Character(
            id = db_manager.generate_new_id(
                model_class=Character,
                unit_id=data.unit_id
            ),
            language_id = unit.get("language_id"),
            **data.model_dump(exclude_none=True)
        )
        result = db_manager.insert(
            obj=character
        )

        if result:
            logger.info(f"Created new character item with ID: {result.id}")
        else:
            logger.error(f"Failed to create new character item: {character.character}")

        return result

    def update(self, char_id: str, data: CharacterDict) -> Character | None:
        """
        Update an existing character item.

        Args:
            char_id: The ID of the character item to update.
            data: CharacterDict containing updated character item details.

        Returns:
            Updated Character object if successful, else None
        """
        existing = self.get_by_id(char_id)
        
        if not existing:
            logger.warning(f"Character item not found: {char_id}")
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
            logger.info(f"Updated character item: {char_id}")
        else:
            logger.error(f"Failed to update character item: {char_id}")
        
        return result

    def delete(self, char_id: str) -> bool:
        """
        Delete a character item by its ID.

        Args:
            char_id: The ID of the character item to delete.

        Returns:
            True if deletion was successful, else False
        """
        # Check if character item exists before deleting
        existing = self.get_by_id(char_id)
        
        if not existing:
            logger.warning(f"Character item not found: {char_id}")
            return False
        
        # Delete from database
        success = db_manager.delete(existing)
        
        if success:
            logger.info(f"Deleted character item: {char_id}")
        else:
            logger.error(f"Failed to delete character item: {char_id}")
        
        return success

    def update_score(self, char_id: str, success: bool) -> Character | None:
        """
        Update character item score based on average of all of its components scores.
        
        This should be called whenever a component's score changes.
        
        Args:
            char_id: The ID of the character item to update
            success: Whether the latest attempt was successful
        
        Returns:
            Updated Character object if successful, None otherwise
        """
        character = self.get_by_id(char_id)
        
        if not character:
            logger.warning(f"Character item not found: {char_id}")
            return None
        
        character.score = update_score(
            current_score=character.score,
            last_seen=character.last_seen,
            success=success
        )
        
        # Update last_seen
        character.last_seen = date.today()

        previous_score = character.score

        if character.score != previous_score:
            if character.unit_id:
                unit_service.update_score(character.unit_id)
                logger.info(f"Updated unit {character.unit_id} score due to character {char_id}")
            if character.language_id:
                language_service.update_score(character.language_id)
                logger.info(f"Updated language {character.language_id} score due to character {char_id}")
        
        # Save changes
        result = db_manager.modify(character)
        
        if result:
            logger.info(f"Updated character item {char_id} score: {result.score}")
        
        return result