from typing import Optional
from httpx import delete
from sqlalchemy.orm import Session
import logging
logger = logging.getLogger(__name__)

from ...models.system_data import UserPreferences
from ...schemas.system_data import UserPreferencesDict
from ...core.database import db_manager

class UserPreferencesService:
    """Service layer for user preferences CRUD operations.

    This class provides convenience methods around the `UserPreferences` model using the
    project's `db_manager` helpers. Methods return `UserPreferencesDict` instances (the
    pydantic schema) where appropriate. See the method docstrings for guidance.
    """
    def _serialize(self, pref_obj: UserPreferences | None, as_dict: bool, include_relations: bool) -> UserPreferencesDict | UserPreferences | None:
        if not as_dict or pref_obj is None:
            return pref_obj
        return pref_obj.to_dict(include_relations=include_relations)
    
    def get_by_id(
        self,
        id: str,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> UserPreferences | UserPreferencesDict | None:
        """Get user preferences by user ID.

        Args:
            user_id (str): The ID of the user whose preferences to retrieve.
            session (Session | None): Optional SQLAlchemy session to use for the query. If None, a new session will be created and managed internally.
            as_dict (bool): If True, return a UserPreferencesDict instance. Otherwise, return a UserPreferences model.
            include_relations (bool): If True, include related objects in the serialized output.

        Returns:
            UserPreferences | UserPreferencesDict | None: The user preferences in the requested format, or None if not found.
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            pref = db_manager.find_one(UserPreferences, filters={"id": id})
            return self._serialize(pref, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get preferences for user {id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def create(
        self,
        data: UserPreferencesDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> UserPreferences | UserPreferencesDict:
        """Create user preferences for a given user ID.

        Args:
            data (UserPreferencesDict): The preferences data to create.
            session (Session | None): Optional SQLAlchemy session to use for the operation. If None, a new session will be created and managed internally.
            as_dict (bool): If True, return a UserPreferencesDict instance. Otherwise, return a UserPreferences model.
            include_relations (bool): If True, include related objects in the serialized output.
        
        Returns:
            UserPreferences | UserPreferencesDict: The created user preferences in the requested format.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()
        try:
            if (existing := db_manager.find_by_attr(model_class=UserPreferences, attr_values={'user_id': data.user_id}, session=session)):
                logger.warning(f"UserPreferences already exists for user {data.user_id}, returning existing preferences with ID {existing.id}")
                return self.update(existing.id, data, session=session, as_dict=as_dict, include_relations=include_relations)
            
            pref = UserPreferences(
                id = db_manager.generate_new_id(model_class=UserPreferences, session=session),
                user_id=data.user_id,
                native_language_iso639_2=data.native_language_iso639_2,
                learning_goals=data.learning_goals,
                preferred_exercise_types=data.preferred_exercise_types
            )
            result = db_manager.insert(pref, session=session)
            if result:
                logger.info(f"Created new UserPreferences object {pref.id} for user {data.user_id}")
            else:
                logger.error(f"Failed to create UserPreferences for user {data.user_id}")

            return self._serialize(pref, as_dict, include_relations)
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to create UserPreferences for user {data.user_id}: {e}")
            raise
        finally:
            if own_session:
                session.close()

    def update(
        self,
        id: str,
        data: UserPreferencesDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> UserPreferences | UserPreferencesDict:
        """Update user preferences for a given user ID.

        Args:
            id (str): The ID of the user preferences to update.
            data (UserPreferencesDict): The updated preferences data.
            session (Session | None): Optional SQLAlchemy session to use for the operation. If None, a new session will be created and managed internally.
            as_dict (bool): If True, return a UserPreferencesDict instance. Otherwise, return a UserPreferences model.
            include_relations (bool): If True, include related objects in the serialized output.

        Returns:
            UserPreferences | UserPreferencesDict: The updated user preferences in the requested format.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()
        try:
            user_pref = db_manager.find_by_attr(
                model_class=UserPreferences,
                attr_values={'id': id},
                session=session
            )
            if not user_pref:
                logger.warning(f"UserPreferences with ID {id} not found for update.")
                return None
            
            # Update fields
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(user_pref, field, value)
            
            result = db_manager.modify(
                obj=user_pref,
                session=session
            )

            if result:
                logger.info(f"Updated UserPreferences item with ID: {result.id}")
            else:
                logger.error(f"Failed to update UserPreferences item with ID: {id}")

            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to update UserPreferences with ID {id}: {e}")
            raise
        finally:
            if own_session:
                session.close()
    
    def delete(
        self,
        id: str,
        session: Optional[Session] = None
    ) -> bool:
        """Delete user preferences by ID.

        Args:
            id (str): The ID of the user preferences to delete.
            session (Session | None): Optional SQLAlchemy session to use for the operation. If None, a new session will be created and managed internally.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()
        try:
            existing = db_manager.get_by_id(UserPreferences, id)
            if not existing:
                return False

            return db_manager.delete(existing)
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to delete UserPreferences with ID {id}: {e}")
            raise
        finally:
            if own_session:
                session.close()