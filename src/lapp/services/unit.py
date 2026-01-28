from datetime import date

import logging

logger = logging.getLogger(__name__)

from ..schemas.element_dict import UnitDict
from ..models import Unit, Character, Vocabulary, Grammar, Exercise
from ..core.database import db_manager

class UnitService:
    def get_all(self, language_id: str) -> list[Unit]:
        """
        Get all units for a specific language.

        Args:
            language_id (str): The id of the language to get all the units from

        Returns:
            List of Unit objects
        """
        return db_manager.find_all(
            model_class=Unit,
            filters={'language_id': language_id}
        )

    def get_by_id(self, unit_id:str) -> Unit | None:
        """
        Get a unit by its ID.

        Args:
            unit_id: The ID of the unit to retrieve.

        Returns:
            Unit object if found, else None
        """
        return db_manager.find_by_attr(
            model_class=Unit,
            attr_values={'id': unit_id}
        )

    def get_by_level(self, language_id: str, level: str) -> list[Unit]:
        """
        Get all units of a specific level among a language.
        
        Args:
            language_id: The id of the language to filter units
            level: Unit level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching Unit objects
        """
        return db_manager.find_all(
            model_class=Unit,
            filters={'level': level, 'language_id': language_id}
        )
    
    def create(self, data: UnitDict) -> Unit | None:
        """
        Create a new unit.

        Args:
            data: UnitDict containing unit details.

        Returns:
            Created Unit object if successful, else None
        """
        unit = Unit(
            id = db_manager.generate_new_id(
                model_class=Unit,
                language_id=data.language_id
            ),
            **data.model_dump(exclude_none=True)
        )
        result = db_manager.insert(
            obj=unit
        )

        if result:
            logger.info(f"Created new unit with ID: {result.id}")
        else:
            logger.error(f"Failed to create new unit: {unit.title}")

        return result

    def update(self, unit_id: str, data: UnitDict) -> Unit | None:
        """
        Update an existing unit.

        Args:
            unit_id: The ID of the unit to update.
            data: UnitDict containing updated language details.

        Returns:
            Updated Unit object if successful, else None
        """
        existing = self.get_by_id(unit_id)
        
        if not existing:
            logger.warning(f"Unit not found: {unit_id}")
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
            logger.info(f"Updated unit: {unit_id}")
        else:
            logger.error(f"Failed to update unit: {unit_id}")
        
        return result

    def delete(self, unit_id: str) -> bool:
        """
        Delete a unit by its ID.

        Args:
            unit_id: The ID of the unit to delete.

        Returns:
            True if deletion was successful, else False
        """
        # Check if unit exists before deleting
        existing = self.get_by_id(unit_id)
        
        if not existing:
            logger.warning(f"Unit not found: {unit_id}")
            return False
        
        # Delete from database
        success = db_manager.delete(existing)
        
        if success:
            logger.info(f"Deleted unit: {unit_id}")
        else:
            logger.error(f"Failed to delete unit: {unit_id}")
        
        return success

    def update_score(self, unit_id: str) -> Unit | None:
        """
        Update unit score based on average of all of its components scores.
        
        This should be called whenever a component's score changes.
        
        Args:
            unit_id: The ID of the unit to update
        
        Returns:
            Updated Unit object if successful, None otherwise
        """
        unit = self.get_by_id(unit_id)
        
        if not unit:
            logger.warning(f"Unit not found: {unit_id}")
            return None
        
        # Get all components for this language
        components = db_manager.find_all(
            model_class=[Vocabulary, Grammar, Character, Exercise],
            filters={'unit_id': unit_id}
        )

        if not components:
            logger.warning(f"No components found for unit: {unit_id}")
            unit.score = 0.0
        else:
            # Calculate average score from all units
            total_score = sum(component.score for component in components)
            unit.score = round(total_score / len(components), 2)
            
            logger.info(
                f"Calculated unit score: {unit.score} "
                f"(from {len(components)} components)"
            )
        
        # Update last_seen
        unit.last_seen = date.today()
        
        # Save changes
        result = db_manager.modify(unit)
        
        if result:
            logger.info(f"Updated unit {unit_id} score: {result.score}")
        
        return result