import logging
from typing import Optional

from sqlalchemy.orm import Session
logger = logging.getLogger(__name__)

from ...schemas.components import WordDict
from ...models.components import Word
from ...core.database import db_manager


class WordService:
    def get_all(self, session: Optional[Session] = None) -> list[Word]:
        """
        Get all words.

        Args:
            None

        Returns:
            List of Word objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            return db_manager.find_all(
                model_class=Word,
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get all words: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(self, word_id: str, session: Optional[Session] = None) -> Word | None:
        """
        Get a word by its ID.

        Args:
            word_id: The ID of the word to retrieve.

        Returns:
            Word object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            return db_manager.find_by_attr(
                model_class=Word,
                attr_values={'id': word_id},
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get word {word_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_word(self, word: str, session: Optional[Session] = None) -> Word | None:
        """
        Get a word by its word value.

        Args:
            word: The word string to retrieve.

        Returns:
            Word object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            return db_manager.find_by_attr(
                model_class=Word,
                attr_values={'word': word},
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get word by word value '{word}': {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def create(self, data: WordDict, session: Optional[Session] = None) -> Word | None:
        """
        Create a new word.

        Args:
            data: WordDict containing word details.

        Returns:
            Created Word object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            word = Word(
                id=db_manager.generate_new_id(model_class=Word, session=session),
                **data.model_dump(exclude_none=True)
            )
            result = db_manager.insert(obj=word, session=session)

            if result:
                logger.info(f"Created new word with ID: {result.id}")
            else:
                logger.error(f"Failed to create new word: {word.word}")

            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to create word: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update(self, word_id: str, data: WordDict, session: Optional[Session] = None) -> Word | None:
        """
        Update an existing word.

        Args:
            word_id: The ID of the word to update.
            data: WordDict containing updated word details.

        Returns:
            Updated Word object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            existing = self.get_by_id(word_id, session=session)

            if not existing:
                logger.warning(f"Word not found: {word_id}")
                return None

            # Only update fields that were provided (partial updates)
            update_data = data.model_dump(exclude_unset=True, exclude_none=True)

            # Update the existing object's attributes
            for key, value in update_data.items():
                setattr(existing, key, value)

            # Save to database
            result = db_manager.modify(existing, session=session)

            if result:
                logger.info(f"Updated word: {word_id}")
            else:
                logger.error(f"Failed to update word: {word_id}")

            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update word {word_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def delete(self, word_id: str, session: Optional[Session] = None) -> bool:
        """
        Delete a word by its ID.

        Args:
            word_id: The ID of the word to delete.

        Returns:
            True if deletion was successful, else False
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            # Check if word exists before deleting
            existing = self.get_by_id(word_id, session=session)

            if not existing:
                logger.warning(f"Word not found: {word_id}")
                return False

            # Delete from database
            success = db_manager.delete(existing, session=session)

            if success:
                logger.info(f"Deleted word: {word_id}")
            else:
                logger.error(f"Failed to delete word: {word_id}")

            return success
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to delete word {word_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()
