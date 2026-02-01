from datetime import date
from typing import Optional
import logging

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

from ...schemas.containers import UnitDict
from ...models.containers import Unit
from ...models.features import Calligraphy, Vocabulary, Grammar, Exercise
from ...core.database import db_manager
from .language import LanguageService

language_service = LanguageService()

class UnitService:
    def get_all(self, language_id: str, session: Optional[Session] = None) -> list[Unit]:
        """
        Get all units for a specific language.

        Args:
            language_id (str): The id of the language to get all the units from

        Returns:
            List of UnitContainer objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            return db_manager.find_all(
                model_class=Unit,
                filters={'language_id': language_id},
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get all units for language {language_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(self, unit_id: str, session: Optional[Session] = None) -> Unit | None:
        """
        Get a unit by its ID.

        Args:
            unit_id: The ID of the unit to retrieve.

        Returns:
            UnitContainer object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            return db_manager.find_by_attr(
                model_class=Unit,
                attr_values={'id': unit_id},
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get unit {unit_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_level(self, level: str, language_id: Optional[str] = None, session: Optional[Session] = None) -> list[Unit]:
        """
        Get all units of a specific level among a language.
        
        Args:
            language_id: The id of the language to filter units
            level: Unit level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching UnitContainer objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            if language_id:
                return db_manager.find_all(
                    model_class=Unit,
                    filters={'level': level, 'language_id': language_id},
                    session=session
                )
            else:
                return db_manager.find_all(
                    model_class=Unit,
                    filters={'level': level},
                    session=session
                )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get units by level {level}: {e}")
            raise
        finally:
            if owns_session:
                session.close()
    
    def create(self, data: UnitDict, session: Optional[Session] = None) -> Unit | None:
        """
        Create a new unit.

        Args:
            data: UnitDict containing unit details.

        Returns:
            Created UnitContainer object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            unit = Unit(
                id = db_manager.generate_new_id(
                    model_class=Unit,
                    session=session
                ),
                **data.model_dump(exclude_none=True)
            )
            result = db_manager.insert(
                obj=unit,
                session=session
            )

            if result:
                logger.info(f"Created new unit with ID: {result.id}")
            else:
                logger.error(f"Failed to create new unit: {unit.title}")

            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to create unit: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update(self, unit_id: str, data: UnitDict, session: Optional[Session] = None) -> Unit | None:
        """
        Update an existing unit.

        Args:
            unit_id: The ID of the unit to update.
            data: UnitDict containing updated language details.

        Returns:
            Updated UnitContainer object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            existing = self.get_by_id(unit_id, session=session)
            
            if not existing:
                logger.warning(f"UnitContainer not found: {unit_id}")
                return None
            
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
                logger.info(f"Updated unit: {unit_id}")
            else:
                logger.error(f"Failed to update unit: {unit_id}")
            
            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update unit {unit_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def delete(self, unit_id: str, session: Optional[Session] = None) -> bool:
        """
        Delete a unit by its ID.

        Args:
            unit_id: The ID of the unit to delete.

        Returns:
            True if deletion was successful, else False
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            # Check if unit exists before deleting
            existing = self.get_by_id(unit_id, session=session)
            
            if not existing:
                logger.warning(f"Unit not found: {unit_id}")
                return False
            
            # Delete from database
            success = db_manager.delete(existing, session=session)
            
            if success:
                logger.info(f"Deleted unit: {unit_id}")
            else:
                logger.error(f"Failed to delete unit: {unit_id}")
            
            return success
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to delete unit {unit_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update_score(self, unit_id: str, session: Optional[Session] = None) -> Unit | None:
        """
        Update unit score based on average of all of its components scores.
        
        This should be called whenever a component's score changes.
        
        Args:
            unit_id: The ID of the unit to update
        
        Returns:
            Updated UnitContainer object if successful, None otherwise
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            unit = self.get_by_id(unit_id, session=session)
            
            if not unit:
                logger.warning(f"UnitContainer not found: {unit_id}")
                return None
            
            # Get all components for this language
            components = db_manager.find_all(
                model_class=[Vocabulary, Grammar, Calligraphy, Exercise],
                filters={'unit_id': unit_id},
                session=session
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
            result = db_manager.modify(unit, session=session)
            if result:
                logger.info(f"Updated unit {unit_id} score: {result.score}")

            if not (language_service.update_score(unit.language_id, session=session)):
                raise Exception(f"Failed to update language score for language {unit.language_id} after unit {unit_id} score update.")
            
            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update unit score for {unit_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()
