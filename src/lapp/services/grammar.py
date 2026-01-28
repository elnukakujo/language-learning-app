from datetime import date
from typing import Optional

import logging

logger = logging.getLogger(__name__)

from ..schemas.element_dict import GrammarDict
from ..models import Grammar
from . import UnitService, LanguageService
from ..core.database import db_manager
from ..utils import update_score

unit_service = UnitService()
language_service = LanguageService()

class GrammarService:
    def get_all(self, language_id: Optional[str], unit_id: Optional[str]) -> list[Grammar]:
        """
        Get all grammars for a specific language or unit.

        Args:
            language_id (Optional[str]): The id of the language to get all the grammars from
            unit_id (Optional[str]): The id of the unit to get all the grammars from

        Returns:
            List of Grammar objects
        """
        assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"
        if language_id:
            return db_manager.find_all(
                model_class=Grammar,
                filters={'language_id': language_id}
            )
        elif unit_id:
            return db_manager.find_all(
                model_class=Grammar,
                filters={'unit_id': unit_id}
            )
        else:
            raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")

    def get_by_id(self, grammar_id:str) -> Grammar | None:
        """
        Get a grammar item by its ID.

        Args:
            grammar_id: The ID of the grammar item to retrieve.

        Returns:
            Grammar object if found, else None
        """
        return db_manager.find_by_attr(
            model_class=Grammar,
            attr_values={'id': grammar_id}
        )

    def get_by_level(self, language_id: Optional[str], unit_id: Optional[str], level: str) -> list[Grammar]:
        """
        Get all grammar items of a specific level among a language.
        
        Args:
            language_id: The id of the language to filter grammar items
            unit_id: The id of the unit to filter grammar items
            level: Grammar level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching Grammar objects
        """
        assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"

        if unit_id:
            return db_manager.find_all(
                model_class=Grammar,
                filters={'level': level, 'unit_id': unit_id}
            )
        elif language_id:
            return db_manager.find_all(
                model_class=Grammar,
                filters={'level': level, 'language_id': language_id}
            )
        else:
            raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")
    
    def create(self, data: GrammarDict) -> Grammar | None:
        """
        Create a new grammar item.

        Args:
            data: GrammarDict containing grammar item details.

        Returns:
            Created Grammar object if successful, else None
        """
        grammar = Grammar(
            **data.model_dump(exclude_none=True)
        )
        result = db_manager.insert(
            obj=grammar
        )

        if result:
            logger.info(f"Created new grammar item with ID: {result.id}")
        else:
            logger.error(f"Failed to create new grammar item: {grammar.title}")

        return result

    def update(self, grammar_id: str, data: GrammarDict) -> Grammar | None:
        """
        Update an existing grammar item.

        Args:
            grammar_id: The ID of the grammar item to update.
            data: GrammarDict containing updated grammars item details.

        Returns:
            Updated Grammar object if successful, else None
        """
        existing = self.get_by_id(grammar_id)
        
        if not existing:
            logger.warning(f"Grammar item not found: {grammar_id}")
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
            logger.info(f"Updated grammar item: {grammar_id}")
        else:
            logger.error(f"Failed to update grammar item: {grammar_id}")
        
        return result

    def delete(self, grammar_id: str) -> bool:
        """
        Delete a grammar item by its ID.

        Args:
            grammar_id: The ID of the grammar item to delete.

        Returns:
            True if deletion was successful, else False
        """
        # Check if grammar item exists before deleting
        existing = self.get_by_id(grammar_id)
        
        if not existing:
            logger.warning(f"Grammar item not found: {grammar_id}")
            return False
        
        # Delete from database
        success = db_manager.delete(existing)
        
        if success:
            logger.info(f"Deleted grammar item: {grammar_id}")
        else:
            logger.error(f"Failed to delete grammar item: {grammar_id}")
        
        return success

    def update_score(self, grammar_id: str, success: bool) -> Grammar | None:
        """
        Update grammar item score based on average of all of its components scores.
        
        This should be called whenever a component's score changes.
        
        Args:
            grammar_id: The ID of the grammar item to update
            success: Whether the latest attempt was successful
        
        Returns:
            Updated Grammar object if successful, None otherwise
        """
        grammar = self.get_by_id(grammar_id)
        
        if not grammar:
            logger.warning(f"Grammar item not found: {grammar_id}")
            return None
        
        previous_score = grammar.score

        grammar.score = update_score(
            current_score=grammar.score,
            last_seen=grammar.last_seen,
            success=success
        )
        
        # Update last_seen
        grammar.last_seen = date.today()

        if grammar.score != previous_score:
            if grammar.unit_id:
                unit_service.update_score(grammar.unit_id)
                logger.info(f"Updated unit {grammar.unit_id} score due to grammar {grammar_id}")
            if grammar.language_id:
                language_service.update_score(grammar.language_id)
                logger.info(f"Updated language {grammar.language_id} score due to grammar {grammar_id}")
        
        # Save changes
        result = db_manager.modify(grammar)
        
        if result:
            logger.info(f"Updated grammar item {grammar_id} score: {result.score}")
        
        return result