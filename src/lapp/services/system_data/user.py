from typing import Optional
from sqlalchemy.orm import Session
import logging
logger = logging.getLogger(__name__)

from ...models.system_data import User
from ...schemas.system_data import UserDict
from ...core.database import db_manager

class UserService:
    """Service layer for user CRUD operations.

    This class provides convenience methods around the `User` model using the
    project's `db_manager` helpers. Methods return `UserDict` instances (the
    pydantic schema) where appropriate. See the method docstrings for guidance.
    """
    def _serialize(self, user_obj: User | None, as_dict: bool, include_relations: bool) -> UserDict | User | None:
        if not as_dict or user_obj is None:
            return user_obj
        return user_obj.to_dict(include_relations=include_relations)
    
    def get_all(
            self,
            session: Session | None = None,
            as_dict: bool = False,
            include_relations: bool = True
        ) -> list[UserDict] | list[User]:
        """Get all users.

        Args:
            session (Session | None): Optional SQLAlchemy session to use for the query. If None, a new session will be created and managed internally.
            as_dict (bool): If True, return a list of UserDict instances. Otherwise, return a list of User models.
            include_relations (bool): If True, include related objects in the serialized output.

        Returns:
            list[UserDict] | list[User]: A list of users in the requested format.
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            users = db_manager.find_all(User)
            return [self._serialize(user, as_dict, include_relations) for user in users]
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get all users: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(
        self,
        user_id: str,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> User | UserDict | None:
        """
        Get a user by its ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            User object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            user = db_manager.find_by_attr(
                model_class=User,
                attr_values={'id': user_id},
                session=session
            )
            return self._serialize(user, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get user {user_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def create(
        self,
        user_data: UserDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> User | UserDict:
        """Create a new user.

        Args:
            user_data: A UserDict containing the data for the new user.
            session: An optional SQLAlchemy session to use for the operation.
            as_dict: If True, return a UserDict instance. Otherwise, return a User model.
            include_relations: If True, include related objects in the serialized output.

        Returns:
            The created User object or UserDict, depending on the as_dict flag.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()
        try:
            # Ensure we have an ORM object to insert
            logger.debug(f"Creating User with data: {user_data}")
            user_id = getattr(user_data, "id", None) or db_manager.generate_new_id(User)
            user_obj = User(
                id=user_id,
                username=user_data.username,
            )
            logger.debug(f"Constructed User ORM object: {user_obj.to_dict()}")

            result = db_manager.insert(
                obj=user_obj,
                session=session
            )

            if result:
                logger.info(f"Created new User item with ID: {result.id}")
            else:
                logger.error(f"Failed to create new User item: {result.username}")

            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to create user: {e}")
            raise
        finally:            
            if own_session:
                session.close()
    
    def update(
        self,
        user_id: str,
        update_data: UserDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> User | UserDict | None:
        """Update an existing user.

        Args:
            user_id: The ID of the user to update.
            update_data: A UserDict containing the updated data for the user.
            session: An optional SQLAlchemy session to use for the operation.
            as_dict: If True, return a UserDict instance. Otherwise, return a User model.
            include_relations: If True, include related objects in the serialized output.

        Returns:
            The updated User object or UserDict, depending on the as_dict flag, or None if the user was not found.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()
        try:
            # Find existing user
            user = db_manager.find_by_attr(
                model_class=User,
                attr_values={'id': user_id},
                session=session
            )
            if not user:
                logger.warning(f"User with ID {user_id} not found for update.")
                return None
            
            # Update fields
            for field, value in update_data.model_dump(exclude_unset=True).items():
                setattr(user, field, value)
            
            result = db_manager.modify(
                obj=user,
                session=session
            )

            if result:
                logger.info(f"Updated User item with ID: {result.id}")
            else:
                logger.error(f"Failed to update User item with ID: {user_id}")

            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to update user {user_id}: {e}")
            raise
        finally:            
            if own_session:
                session.close()

    def delete(
        self,
        user_id: str,
        session: Optional[Session] = None
    ) -> bool:
        """Delete a user by its ID.

        Args:
            user_id: The ID of the user to delete.

        Returns:
            True if the user was deleted, False if the user was not found.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()
        try:
            # Find existing user
            user = db_manager.find_by_attr(
                model_class=User,
                attr_values={'id': user_id},
                session=session
            )

            result = db_manager.delete(
                user,
                session=session
            )
            if result:
                logger.info(f"Deleted User item with ID: {user_id}")
            else:
                logger.warning(f"User with ID {user_id} not found for deletion.")
            return result
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to delete user {user_id}: {e}")
            raise
        finally:            
            if own_session:
                session.close()