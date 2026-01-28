from datetime import date

import logging
logger = logging.getLogger(__name__)

from ..schemas.element_dict import LanguageDict
from ..models import Language, Unit
from ..core.database import db_manager

class LanguageService:
    def get_all(self) -> list[Language]:
        """
        Get all languages.

        Args:
            None

        Returns:
            List of Language objects
        """
        return db_manager.find_all(
            model_class=Language
        )

    def get_by_id(self, language_id:str) -> Language | None:
        """
        Get a language by its ID.

        Args:
            language_id: The ID of the language to retrieve.

        Returns:
            Language object if found, else None
        """
        return db_manager.find_by_attr(
            model_class=Language,
            attr_values={'id': language_id}
        )

    def get_by_level(self, level: str) -> list[Language]:
        """
        Get all languages of a specific level.
        
        Args:
            level: Language level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching Language objects
        """
        return db_manager.find_all(
            model_class=Language,
            filters={'level': level}
        )
    
    def create(self, data: LanguageDict) -> Language | None:
        """
        Create a new language.

        Args:
            data: LanguageDict containing language details.

        Returns:
            Created Language object if successful, else None
        """
        language = Language(
            id = db_manager.generate_new_id(model_class=Language),
            **data.model_dump(exclude_none=True)
        )
        result = db_manager.insert(
            obj=language
        )

        if result:
            logger.info(f"Created new language with ID: {result.id}")
        else:
            logger.error(f"Failed to create new language: {language.name}")

        return result

    def update(self, language_id: str, data: LanguageDict) -> Language | None:
        """
        Update an existing language.

        Args:
            language_id: The ID of the language to update.
            data: LanguageDict containing updated language details.

        Returns:
            Updated Language object if successful, else None
        """
        existing = self.get_by_id(language_id)
        
        if not existing:
            logger.warning(f"Language not found: {language_id}")
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
            logger.info(f"Updated language: {language_id}")
        else:
            logger.error(f"Failed to update language: {language_id}")
        
        return result

    def delete(self, language_id: str) -> bool:
        """
        Delete a language by its ID.

        Args:
            language_id: The ID of the language to delete.

        Returns:
            True if deletion was successful, else False
        """
        # Check if language exists before deleting
        existing = self.get_by_id(language_id)
        
        if not existing:
            logger.warning(f"Language not found: {language_id}")
            return False
        
        # Delete from database
        success = db_manager.delete(existing)
        
        if success:
            logger.info(f"Deleted language: {language_id}")
        else:
            logger.error(f"Failed to delete language: {language_id}")
        
        return success

    def update_score(self, language_id: str) -> Language | None:
        """
        Update language score based on average of all unit scores.
        
        This should be called whenever a unit's score changes.
        
        Args:
            language_id: The ID of the language to update
        
        Returns:
            Updated Language object if successful, None otherwise
        """
        language = self.get_by_id(language_id)
        
        if not language:
            logger.warning(f"Language not found: {language_id}")
            return None
        
        # Get all units for this language
        units = db_manager.find_all(
            model_class=Unit,
            filters={'language_id': language_id}
        )
        
        if not units:
            logger.warning(f"No units found for language: {language_id}")
            language.score = 0.0
        else:
            # Calculate average score from all units
            total_score = sum(unit.score for unit in units)
            language.score = round(total_score / len(units), 2)
            
            logger.info(
                f"Calculated language score: {language.score} "
                f"(from {len(units)} units)"
            )
        
        # Update last_seen
        language.last_seen = date.today()
        
        # Save changes
        result = db_manager.modify(language)
        
        if result:
            logger.info(f"Updated language {language_id} score: {result.score}")
        
        return result