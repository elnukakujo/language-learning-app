from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

import logging
logger = logging.getLogger(__name__)

from ...schemas.features import CalligraphyDict
from ...models.features import Calligraphy
from ...core.database import db_manager
from ..containers import UnitService, LanguageService
from ..components import CharacterService, WordService
from ...utils import update_score

unit_service = UnitService()
language_service = LanguageService()
character_service = CharacterService()
word_service = WordService()

class CalligraphyService:
    def _serialize(self, calligraphy: Calligraphy | None, as_dict: bool, include_relations: bool) -> Calligraphy | dict | None:
        if not as_dict or calligraphy is None:
            return calligraphy
        return calligraphy.to_dict(include_relations=include_relations)

    def _serialize_list(self, calligraphies: list[Calligraphy], as_dict: bool, include_relations: bool) -> list[Calligraphy] | list[dict]:
        if not as_dict:
            return calligraphies
        return [calligraphy.to_dict(include_relations=include_relations) for calligraphy in calligraphies]

    def get_all(
        self,
        language_id: Optional[str] = None,
        unit_id: Optional[str] = None,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> list[Calligraphy] | list[dict]:
        """
        Get all calligraphies for a specific language or unit.

        Args:
            language_id (Optional[str]=None): The id of the language to get all the calligraphies from
            unit_id (Optional[str]=None): The id of the unit to get all the calligraphies from
        Returns:
            List of Calligraphy objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"
            if language_id:
                units = unit_service.get_all(language_id=language_id, session=session)

                calligraphies = []
                for unit in units:
                    calligraphies.extend(
                        db_manager.find_all(
                            model_class=Calligraphy,
                            filters={'unit_id': unit.id},
                            session=session
                        )
                    )
                return self._serialize_list(calligraphies, as_dict, include_relations)
            elif unit_id:
                calligraphies = db_manager.find_all(
                    model_class=Calligraphy,
                    filters={'unit_id': unit_id},
                    session=session
                )
                return self._serialize_list(calligraphies, as_dict, include_relations)
            else:
                raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get all calligraphies: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(
        self,
        calligraphy_id: str,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Calligraphy | dict | None:
        """
        Get a Calligraphy item by its ID.

        Args:
            calligraphy_id: The ID of the Calligraphy item to retrieve.

        Returns:
            Calligraphy object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            calligraphy = db_manager.find_by_attr(
                model_class=Calligraphy,
                attr_values={'id': calligraphy_id},
                session=session
            )
            return self._serialize(calligraphy, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get calligraphy by id: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_level(
        self,
        level: str,
        language_id: Optional[str] = None,
        unit_id: Optional[str] = None,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> list[Calligraphy] | list[dict]:
        """
        Get all Calligraphy items of a specific level among a language.
        
        Args:
            language_id: The id of the language to filter Calligraphy items
            unit_id: The id of the unit to filter Calligraphy items
            level: Calligraphy level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching Calligraphy objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"

            if language_id:
                units = unit_service.get_all(language_id=language_id, session=session)

                calligraphies = []
                for unit in units:
                    calligraphies.extend(
                        db_manager.find_all(
                            model_class=Calligraphy,
                            filters={'level':level ,'unit_id': unit.id},
                            session=session
                        )
                    )
                return self._serialize_list(calligraphies, as_dict, include_relations)
            elif unit_id:
                calligraphies = db_manager.find_all(
                    model_class=Calligraphy,
                    filters={'level': level, 'unit_id': unit_id},
                    session=session
                )
                return self._serialize_list(calligraphies, as_dict, include_relations)
            else:
                raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get_by_level calligraphies: {e}")
            raise
        finally:
            if owns_session:
                session.close()
    
    def create(
        self,
        data: CalligraphyDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Calligraphy | dict | None:
        """
        Create a new Calligraphy item.

        Args:
            data: CalligraphyDict containing calligraphy item details.

        Returns:
            Created Calligraphy object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            unit = unit_service.get_by_id(data.unit_id, session=session)

            if not unit:
                logger.warning(f"Cannot create Calligraphy item, unit not found: {data.unit_id}")
                return None
            
            # Create Character using CharacterService
            character = character_service.create(data.character, session=session)
            if not character:
                logger.error(f"Failed to create character for calligraphy")
                return None
            
            # Ensure character is loaded in session
            if character and not session.get(Calligraphy.character.property.mapper.class_, character.id):
                raise ValueError(f"Character not found in session after creation for calligraphy")
            
            # Create example_word using WordService if provided
            example_word = None
            if data.example_word:
                example_word = word_service.create(data.example_word, session=session)
                if not example_word:
                    logger.warning(f"Failed to create example_word for calligraphy")

            # Ensure example_word is loaded in session
            if example_word and not session.get(Calligraphy.example_word.property.mapper.class_, example_word.id):
                raise ValueError(f"Example word not found in session after creation for calligraphy")
            
            calligraphy = Calligraphy(
                id = db_manager.generate_new_id(
                    model_class=Calligraphy,
                    session=session
                ),
                **data.model_dump(exclude={'character', 'example_word'}, exclude_none=True)
            )

            calligraphy.character_id = character.id
            calligraphy.character = character
            calligraphy.example_word_id = example_word.id if example_word else None
            calligraphy.example_word = example_word
            
            result = db_manager.insert(
                obj=calligraphy,
                session=session
            )

            if result:
                logger.info(f"Created new Calligraphy item with ID: {result.id}")
            else:
                logger.error(f"Failed to create new Calligraphy item")

            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to create calligraphy: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update(
        self,
        calligraphy_id: str,
        data: CalligraphyDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Calligraphy | dict | None:
        """
        Update an existing Calligraphy item.

        Args:
            calligraphy_id: The ID of the Calligraphy item to update.
            data: calligraphyDict containing updated Calligraphy item details.

        Returns:
            Updated Calligraphy object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            existing = self.get_by_id(calligraphy_id, session=session)
            
            if not existing:
                logger.warning(f"Calligraphy item not found: {calligraphy_id}")
                return None
            
            # Handle Character update through CharacterService if provided
            if data.character is not None:
                updated_character = character_service.update(existing.character_id, data.character, session=session)
                if not updated_character:
                    logger.error(f"Failed to update character for calligraphy: {calligraphy_id}")
                    return None
                existing.character = updated_character
            
            # Handle example_word update through WordService if provided
            if data.example_word is not None:
                if existing.example_word_id:
                    # Update existing word
                    updated_word = word_service.update(existing.example_word_id, data.example_word, session=session)
                    if updated_word:
                        existing.example_word = updated_word
                else:
                    # Create new word
                    new_word = word_service.create(data.example_word, session=session)
                    if new_word:
                        existing.example_word_id = new_word.id
                        existing.example_word = new_word
            
            # Only update fields that were provided (partial updates)
            update_data = data.model_dump(exclude_unset=True, exclude_none=True)
            
            # Remove nested objects from update_data
            update_data.pop('character', None)
            update_data.pop('example_word', None)
            
            # Update the existing object's attributes
            for key, value in update_data.items():
                if key not in ('character_id', 'example_word_id'):  # Don't overwrite if already set
                    setattr(existing, key, value)
            
            # Update last_seen
            existing.last_seen = date.today()
            
            # Save to database
            result = db_manager.modify(existing, session=session)
            
            if result:
                logger.info(f"Updated Calligraphy item: {calligraphy_id}")
            else:
                logger.error(f"Failed to update Calligraphy item: {calligraphy_id}")
            
            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update calligraphy: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def delete(self, calligraphy_id: str, session: Optional[Session] = None) -> bool:
        """
        Delete a Calligraphy item by its ID.

        Args:
            calligraphy_id: The ID of the Calligraphy item to delete.
        Returns:
            True if deletion was successful, else False
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            # Check if Calligraphy item exists before deleting
            existing = self.get_by_id(calligraphy_id, session=session)
            
            if not existing:
                logger.warning(f"Calligraphy item not found: {calligraphy_id}")
                return False
            
            # Delete from database
            success = db_manager.delete(existing, session=session)
            
            if success:
                logger.info(f"Deleted Calligraphy item: {calligraphy_id}")
            else:
                logger.error(f"Failed to delete Calligraphy item: {calligraphy_id}")
            
            return success
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to delete calligraphy: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update_score(
        self,
        calligraphy_id: str,
        success: bool,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Calligraphy | dict | None:
        """
        Update Calligraphy item score based on average of all of its components scores.
        
        This should be called whenever a component's score changes.
        
        Args:
            calligraphy_id: The ID of the Calligraphy item to update
            success: Whether the latest attempt was successful
        
        Returns:
            Updated Calligraphy object if successful, None otherwise
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            calligraphy = self.get_by_id(calligraphy_id, session=session)

            if not calligraphy:
                logger.warning(f"Calligraphy item not found: {calligraphy_id}")
                return None
            
            previous_score = calligraphy.score

            calligraphy.score = update_score(
                score=calligraphy.score,
                last_seen=calligraphy.last_seen,
                success=success
            )
            
            # Update last_seen
            calligraphy.last_seen = date.today()
            
            # Save changes
            result = db_manager.modify(calligraphy, session=session)
            
            if result:
                logger.info(f"Updated Calligraphy item {calligraphy_id} score: {result.score}")

            if calligraphy.score != previous_score:
                if calligraphy.unit_id:
                    unit_service.update_score(calligraphy.unit_id, session=session)
                    logger.info(f"Updated unit {calligraphy.unit_id} score due to calligraphy {calligraphy_id}")
            
            
            
            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update calligraphy score: {e}")
            raise
        finally:
            if owns_session:
                session.close()
