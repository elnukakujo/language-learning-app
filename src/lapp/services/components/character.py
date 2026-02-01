from datetime import date
import logging
from typing import Optional

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

from ...schemas.components import CharacterDict
from ...models.components import Character
from ...core.database import db_manager


class CharacterService:
    def get_all(self, session: Optional[Session] = None) -> list[Character]:
        """
        Get all characters.

        Args:
            None

        Returns:
            List of Character objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            return db_manager.find_all(
                model_class=Character,
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get all characters: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(self, character_id: str, session: Optional[Session] = None) -> Character | None:
        """
        Get a character by its ID.

        Args:
            character_id: The ID of the character to retrieve.

        Returns:
            Character object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            return db_manager.find_by_attr(
                model_class=Character,
                attr_values={'id': character_id},
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get character {character_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_character(self, character: str, session: Optional[Session] = None) -> Character | None:
        """
        Get a character by its character value.

        Args:
            character: The character string to retrieve.

        Returns:
            Character object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            return db_manager.find_by_attr(
                model_class=Character,
                attr_values={'character': character},
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get character by character value '{character}': {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def create(self, data: CharacterDict, session: Optional[Session] = None) -> Character | None:
        """
        Create a new character.

        Args:
            data: CharacterDict containing character details.

        Returns:
            Created Character object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            if existing := self.get_by_character(data.character, session=session):
                logger.info(f"Character already exists: {data.character} with ID: {existing.id}")
                return existing
            
            character = Character(
                id=db_manager.generate_new_id(model_class=Character, session=session),
                **data.model_dump(exclude_none=True)
            )
            result = db_manager.insert(obj=character, session=session)

            if result:
                logger.info(f"Created new character with ID: {result.id}")
            else:
                logger.error(f"Failed to create new character: {character.character}")

            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to create character: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update(self, character_id: str, data: CharacterDict, session: Optional[Session] = None) -> Character | None:
        """
        Update an existing character.

        Args:
            character_id: The ID of the character to update.
            data: CharacterDict containing updated character details.

        Returns:
            Updated Character object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            existing = self.get_by_id(character_id, session=session)

            if not existing:
                logger.warning(f"Character not found: {character_id}")
                return None

            # Only update fields that were provided (partial updates)
            update_data = data.model_dump(exclude_unset=True, exclude_none=True)

            # Update the existing object's attributes
            for key, value in update_data.items():
                setattr(existing, key, value)

            # Save to database
            result = db_manager.modify(existing, session=session)

            if result:
                logger.info(f"Updated character: {character_id}")
            else:
                logger.error(f"Failed to update character: {character_id}")

            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update character {character_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def delete(self, character_id: str, session: Optional[Session] = None) -> bool:
        """
        Delete a character by its ID.

        Args:
            character_id: The ID of the character to delete.

        Returns:
            True if deletion was successful, else False
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            # Check if character exists before deleting
            existing = self.get_by_id(character_id, session=session)

            if not existing:
                logger.warning(f"Character not found: {character_id}")
                return False

            # Delete from database
            success = db_manager.delete(existing, session=session)

            if success:
                logger.info(f"Deleted character: {character_id}")
            else:
                logger.error(f"Failed to delete character: {character_id}")

            return success
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to delete character {character_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()
