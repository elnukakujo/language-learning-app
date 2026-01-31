from datetime import date
from typing import Optional

import logging
logger = logging.getLogger(__name__)

from ..schemas.features import CalligraphyDict
from ..models.features import Calligraphy
from ..core.database import db_manager
from . import UnitService, LanguageService
from ..utils import update_score

unit_service = UnitService()
language_service = LanguageService()

class CalligraphyService:
    def get_all(self, language_id: Optional[str]=None, unit_id: Optional[str]=None) -> list[Calligraphy]:
        """
        Get all calligraphies for a specific language or unit.

        Args:
            language_id (Optional[str]=None): The id of the language to get all the calligraphies from
            unit_id (Optional[str]=None): The id of the unit to get all the calligraphies from
        Returns:
            List of Calligraphy objects
        """
        assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"
        if language_id:
            units = unit_service.get_all(language_id=language_id)

            calligraphies = []
            for unit in units:
                calligraphies.extend(
                    db_manager.find_all(
                        model_class=Calligraphy,
                        filters={'unit_id': unit.id}
                    )
                )
            return calligraphies
        elif unit_id:
            return db_manager.find_all(
                model_class=Calligraphy,
                filters={'unit_id': unit_id}
            )
        else:
            raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")

    def get_by_id(self, char_id:str) -> Calligraphy | None:
        """
        Get a Calligraphy item by its ID.

        Args:
            char_id: The ID of the Calligraphy item to retrieve.

        Returns:
            Calligraphy object if found, else None
        """
        return db_manager.find_by_attr(
            model_class=Calligraphy,
            attr_values={'id': char_id}
        )

    def get_by_level(self, level: str, language_id: Optional[str]=None, unit_id: Optional[str]=None) -> list[Calligraphy]:
        """
        Get all Calligraphy items of a specific level among a language.
        
        Args:
            language_id: The id of the language to filter Calligraphy items
            unit_id: The id of the unit to filter Calligraphy items
            level: Calligraphy level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching Calligraphy objects
        """
        assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"

        if language_id:
            units = unit_service.get_all(language_id=language_id)

            calligraphies = []
            for unit in units:
                calligraphies.extend(
                    db_manager.find_all(
                        model_class=Calligraphy,
                        filters={'level':level ,'unit_id': unit.id}
                    )
                )
            return calligraphies
        elif unit_id:
            return db_manager.find_all(
                model_class=Calligraphy,
                filters={'level': level, 'unit_id': unit_id}
            )
        else:
            raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")
    
    def create(self, data: CalligraphyDict) -> Calligraphy | None:
        """
        Create a new Calligraphy item.

        Args:
            data: CalligraphyDict containing calligraphy item details.

        Returns:
            Created Calligraphy object if successful, else None
        """
        unit = unit_service.get_by_id(data.unit_id)

        if not unit:
            logger.warning(f"Cannot create Calligraphy item, unit not found: {data.unit_id}")
            return None
        
        calligraphy = Calligraphy(
            id = db_manager.generate_new_id(
                model_class=Calligraphy
            ),
            **data.model_dump(exclude_none=True)
        )
        result = db_manager.insert(
            obj=calligraphy
        )

        if result:
            logger.info(f"Created new Calligraphy item with ID: {result.id}")
        else:
            logger.error(f"Failed to create new Calligraphy item: {calligraphy.calligraphy}")

        return result

    def update(self, char_id: str, data: CalligraphyDict) -> Calligraphy | None:
        """
        Update an existing Calligraphy item.

        Args:
            char_id: The ID of the Calligraphy item to update.
            data: calligraphyDict containing updated Calligraphy item details.

        Returns:
            Updated Calligraphy object if successful, else None
        """
        existing = self.get_by_id(char_id)
        
        if not existing:
            logger.warning(f"Calligraphy item not found: {char_id}")
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
            logger.info(f"Updated Calligraphy item: {char_id}")
        else:
            logger.error(f"Failed to update Calligraphy item: {char_id}")
        
        return result

    def delete(self, char_id: str) -> bool:
        """
        Delete a Calligraphy item by its ID.

        Args:
            char_id: The ID of the Calligraphy item to delete.
        Returns:
            True if deletion was successful, else False
        """
        # Check if Calligraphy item exists before deleting
        existing = self.get_by_id(char_id)
        
        if not existing:
            logger.warning(f"Calligraphy item not found: {char_id}")
            return False
        
        # Delete from database
        success = db_manager.delete(existing)
        
        if success:
            logger.info(f"Deleted Calligraphy item: {char_id}")
        else:
            logger.error(f"Failed to delete Calligraphy item: {char_id}")
        
        return success

    def update_score(self, char_id: str, success: bool) -> Calligraphy | None:
        """
        Update Calligraphy item score based on average of all of its components scores.
        
        This should be called whenever a component's score changes.
        
        Args:
            char_id: The ID of the Calligraphy item to update
            success: Whether the latest attempt was successful
        
        Returns:
            Updated Calligraphy object if successful, None otherwise
        """
        calligraphy = self.get_by_id(char_id)
        
        if not calligraphy:
            logger.warning(f"Calligraphy item not found: {char_id}")
            return None
        
        calligraphy.score = update_score(
            current_score=calligraphy.score,
            last_seen=calligraphy.last_seen,
            success=success
        )
        
        # Update last_seen
        calligraphy.last_seen = date.today()

        previous_score = calligraphy.score

        if calligraphy.score != previous_score:
            if calligraphy.unit_id:
                unit_service.update_score(calligraphy.unit_id)
                logger.info(f"Updated unit {calligraphy.unit_id} score due to calligraphy {char_id}")
            if calligraphy.language_id:
                language_service.update_score(calligraphy.language_id)
                logger.info(f"Updated language {calligraphy.language_id} score due to calligraphy {char_id}")
        
        # Save changes
        result = db_manager.modify(calligraphy)
        
        if result:
            logger.info(f"Updated Calligraphy item {char_id} score: {result.score}")
        
        return result