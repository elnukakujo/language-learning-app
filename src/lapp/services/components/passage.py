from datetime import date
import logging
from typing import Optional

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

from ...schemas.components import PassageDict
from ...models.components import Passage
from ...core.database import db_manager


class PassageService:
    def get_all(self, session: Optional[Session] = None) -> list[Passage]:
        """
        Get all passages.

        Args:
            None

        Returns:
            List of Passage objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            return db_manager.find_all(
                model_class=Passage,
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get all passages: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(self, passage_id: str, session: Optional[Session] = None) -> Passage | None:
        """
        Get a passage by its ID.

        Args:
            passage_id: The ID of the passage to retrieve.

        Returns:
            Passage object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            return db_manager.find_by_attr(
                model_class=Passage,
                attr_values={'id': passage_id},
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get passage {passage_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_vocabulary_id(self, vocabulary_id: str, session: Optional[Session] = None) -> list[Passage]:
        """
        Get all passages for a specific vocabulary.

        Args:
            vocabulary_id: The ID of the vocabulary to get passages for.

        Returns:
            List of Passage objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            return db_manager.find_all(
                model_class=Passage,
                filters={'vocabulary_id': vocabulary_id},
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get passages for vocabulary {vocabulary_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_grammar_id(self, grammar_id: str, session: Optional[Session] = None) -> list[Passage]:
        """
        Get all passages for a specific grammar.

        Args:
            grammar_id: The ID of the grammar to get passages for.

        Returns:
            List of Passage objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            return db_manager.find_all(
                model_class=Passage,
                filters={'grammar_id': grammar_id},
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get passages for grammar {grammar_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def create(self, data: PassageDict, session: Optional[Session] = None) -> Passage | None:
        """
        Create a new passage.

        Args:
            data: PassageDict containing passage details.

        Returns:
            Created Passage object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            passage = Passage(
                id=db_manager.generate_new_id(model_class=Passage, session=session),
                **data.model_dump(exclude_none=True)
            )
            result = db_manager.insert(obj=passage, session=session)

            if result:
                logger.info(f"Created new passage with ID: {result.id}")
            else:
                logger.error(f"Failed to create new passage")

            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to create passage: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update(self, passage_id: str, data: PassageDict, session: Optional[Session] = None) -> Passage | None:
        """
        Update an existing passage.

        Args:
            passage_id: The ID of the passage to update.
            data: PassageDict containing updated passage details.

        Returns:
            Updated Passage object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            existing = self.get_by_id(passage_id, session=session)

            if not existing:
                logger.warning(f"Passage not found: {passage_id}")
                return None

            # Only update fields that were provided (partial updates)
            update_data = data.model_dump(exclude_unset=True, exclude_none=True)

            # Update the existing object's attributes
            for key, value in update_data.items():
                setattr(existing, key, value)

            # Save to database
            result = db_manager.modify(existing, session=session)

            if result:
                logger.info(f"Updated passage: {passage_id}")
            else:
                logger.error(f"Failed to update passage: {passage_id}")

            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update passage {passage_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def delete(self, passage_id: str, session: Optional[Session] = None) -> bool:
        """
        Delete a passage by its ID.

        Args:
            passage_id: The ID of the passage to delete.

        Returns:
            True if deletion was successful, else False
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            # Check if passage exists before deleting
            existing = self.get_by_id(passage_id, session=session)

            if not existing:
                logger.warning(f"Passage not found: {passage_id}")
                return False

            # Delete from database
            success = db_manager.delete(existing, session=session)

            if success:
                logger.info(f"Deleted passage: {passage_id}")
            else:
                logger.error(f"Failed to delete passage: {passage_id}")

            return success
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to delete passage {passage_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()
