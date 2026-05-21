from typing import Optional
from sqlalchemy.orm import Session

import logging
logger = logging.getLogger(__name__)

from ...schemas.system_data import TagDict
from ...models.system_data import Tag
from ...core.database import db_manager
from ...utils import resolve_element_model

class TagService:
    """Service layer for tag CRUD operations.

    This class provides convenience methods around the `Tag` model using the
    project's `db_manager` helpers. Methods return `TagDict` instances (the
    pydantic schema) where appropriate. See the method docstrings for guidance.
    """

    def _serialize(self, tag_obj: Tag | None, as_dict: bool, include_relations: bool) -> TagDict | dict | None:
        if not as_dict or tag_obj is None:
            return tag_obj
        return tag_obj.to_dict(include_relations=include_relations)

    def get_by_id(
            self, 
            tag_id: str,
            session: Optional[Session] = None,
            as_dict: bool = False,
            include_relations: bool = True
        ) -> Tag | dict:
        """Retrieve a tag by its ID.

        Returns the `TagDict` if found, otherwise `None`.
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            tag_obj = db_manager.get_by_id(Tag, tag_id)
            return self._serialize(tag_obj, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get tag by ID {tag_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_user_id(
            self,
            user_id: str,
            session: Optional[Session] = None,
            as_dict: bool = False,
            include_relations: bool = True
        ) -> list[Tag] | list[dict]:
        """Return all tags that belong to a given `user_id`.

        Returns an empty list when no tags are found.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()
        try:
            objs = db_manager.find_all(Tag, filters={"user_id": user_id})
            return [self._serialize(obj, as_dict, include_relations) for obj in objs]
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to get tags by user ID {user_id}: {e}")
            raise
        finally:            
            if own_session:
                session.close()

    def create(
            self,
            tag_data: TagDict,
            session: Optional[Session] = None,
            as_dict: bool = False,
            include_relations: bool = True
        ) -> Tag | dict:
        """Create a new tag.

        If `tag_data.id` is not provided or empty, a new id will be generated
        using `db_manager.generate_new_id(Tag)`. Returns the created
        `TagDict` on success or `None` on failure.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()
        try:
            # Ensure we have an ORM object to insert
            tag_id = getattr(tag_data, "id", None) or db_manager.generate_new_id(Tag)
            tag_obj = Tag(
                id=tag_id,
                user_id=tag_data.user_id,
                name=tag_data.name,
                color=tag_data.color,
                description=tag_data.description,
            )

            result = db_manager.insert(
                obj=tag_obj,
                session=session
            )

            if result:
                logger.info(f"Created new Tag item with ID: {result.id}")
            else:
                logger.error(f"Failed to create new Tag item: {tag_obj.name}")

            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to create tag: {e}")
            raise
        finally:            
            if own_session:
                session.close()

    def update(
            self, 
            tag_id: str, 
            tag_data: TagDict,
            session: Optional[Session] = None,
            as_dict: bool = False,
            include_relations: bool = True
        ) -> Tag | dict:
        """Update an existing tag by `tag_id`.

        Returns the updated `TagDict` on success or `None` if the tag does not
        exist or the update fails.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()

        try:
            existing = db_manager.get_by_id(Tag, tag_id)
            if not existing:
                return None

            # Update fields
            existing.user_id = tag_data.user_id
            existing.name = tag_data.name
            existing.color = tag_data.color
            existing.description = tag_data.description

            modified = db_manager.modify(existing)
            return self._serialize(modified, as_dict, include_relations)
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to update tag with ID {tag_id}: {e}")
            raise
        finally:
            if own_session:
                session.close()

    def delete(
        self, 
        tag_id: str,
        session: Optional[Session] = None
    ) -> bool:
        """Delete the tag identified by `tag_id`.

        Returns `True` when deletion succeeds, `False` otherwise.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()

        try:
            existing = db_manager.get_by_id(Tag, tag_id)
            if not existing:
                return False

            return db_manager.delete(existing)
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to delete tag with ID {tag_id}: {e}")
            raise
        finally:
            if own_session:
                session.close()

    def add_tag_to_element(
        self,
        tag_id: str,
        element_id: str,
        session: Optional[Session] = None
    ) -> bool:
        """Associate a tag with an element.

        Uses ORM relationships through `db_manager` rather than raw SQL.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()
        
        try:
            tag_obj = db_manager.get_by_id(Tag, tag_id)
            if not tag_obj:
                return False

            element_model = resolve_element_model(element_id)
            if not element_model:
                return False

            element_obj = db_manager.get_by_id(element_model, element_id)
            if not element_obj:
                return False

            # avoid duplicates
            if any(t.id == tag_id for t in element_obj.tags):
                return True

            element_obj.tags.append(tag_obj)
            modified = db_manager.modify(element_obj)
            return bool(modified)
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to add tag {tag_id} to element {element_id}: {e}")
            raise
        finally:
            if own_session:
                session.close()

    def remove_tag_from_element(self, tag_id: str, element_id: str, session: Optional[Session] = None) -> bool:
        """Remove a tag association from an element.

        Uses ORM relationships through `db_manager` rather than raw SQL.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()

        try:
            tag_obj = db_manager.get_by_id(Tag, tag_id)
            if not tag_obj:
                return False

            element_model = resolve_element_model(element_id)
            if not element_model:
                return False

            element_obj = db_manager.get_by_id(element_model, element_id)
            if not element_obj:
                return False

            if not any(t.id == tag_id for t in element_obj.tags):
                return False

            element_obj.tags = [tag for tag in element_obj.tags if tag.id != tag_id]
            modified = db_manager.modify(element_obj)
            return bool(modified)
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to remove tag {tag_id} from element {element_id}: {e}")
            raise
        finally:
            if own_session:
                session.close()