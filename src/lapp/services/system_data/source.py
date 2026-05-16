from typing import Optional, Type
from sqlalchemy.orm import Session

import logging
logger = logging.getLogger(__name__)

from ...schemas.system_data import SourceDict
from ...models.system_data import Source
from ...core.database import db_manager


class SourceService:
    """Service layer for source CRUD operations.

    This class provides convenience methods around the `Source` model using the
    project's `db_manager` helpers. Methods return `SourceDict` instances (the
    pydantic schema) where appropriate.
    
    Sources are metadata objects (e.g., textbook, movie, article) that can be
    associated with any element. The `source_type` field describes the source
    category and is independent of element associations.
    """

    def _serialize(self, source_obj: Source | None, as_dict: bool, include_relations: bool) -> SourceDict | dict | None:
        """Convert a Source ORM object to dict or return ORM object based on as_dict flag."""
        if not as_dict or source_obj is None:
            return source_obj
        return source_obj.to_dict(include_relations=include_relations)
    
    def _resolve_element_model(self, element_id: str) -> Optional[Type]:
        """Map an element id string to the corresponding ORM model.
        
        ID Format:
        - Language: "lang_L{n}"
        - Lesson: "lesson_L{n}"
        - Vocabulary: "voc_V{n}"
        - Grammar: "gram_G{n}"
        - Calligraphy: "call_C{n}"
        - Exercise: "ex_E{n}"
        - Character: "char_C{n}"
        - Word: "word_W{n}"
        - Passage: "pass_P{n}"
        """
        from ...models.features import Vocabulary, Grammar, Calligraphy, Exercise
        from ...models.components import Word, Passage, Character
        from ...models.containers import Language, Lesson
        model_map = {
            "voc": Vocabulary,
            "gram": Grammar,
            "call": Calligraphy,
            "exer": Exercise,
            "word": Word,
            "pass": Passage,
            "char": Character,
            "lang": Language,
            "lesson": Lesson
        }
        return model_map.get(element_id.split("_")[0])

    def get_by_id(
            self, 
            source_id: str,
            session: Optional[Session] = None,
            as_dict: bool = False,
            include_relations: bool = True
        ) -> Source | dict:
        """Retrieve a source by its ID.

        Returns the `SourceDict` if found, otherwise `None`.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()
        
        try:
            source_obj = db_manager.get_by_id(Source, source_id)
            return self._serialize(source_obj, as_dict, include_relations)
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to get source by ID {source_id}: {e}")
            raise
        finally:
            if own_session:
                session.close()

    def get_by_user_id(
            self,
            user_id: str,
            session: Optional[Session] = None,
            as_dict: bool = False,
            include_relations: bool = True
        ) -> list[Source] | list[dict]:
        """Return all sources that belong to a given `user_id`.

        Returns an empty list when no sources are found.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()
        try:
            objs = db_manager.find_all(Source, filters={"user_id": user_id})
            return [self._serialize(obj, as_dict, include_relations) for obj in objs]
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to get sources by user ID {user_id}: {e}")
            raise
        finally:            
            if own_session:
                session.close()

    def create(
            self,
            source_data: SourceDict,
            session: Optional[Session] = None,
            as_dict: bool = False,
            include_relations: bool = True
        ) -> Source | dict:
        """Create a new source.

        If `source_data.id` is not provided or empty, a new id will be generated
        using `db_manager.generate_new_id(Source)`. Returns the created
        `SourceDict` on success or `None` on failure.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()
        try:
            # Ensure we have an ORM object to insert
            source_id = getattr(source_data, "id", None) or db_manager.generate_new_id(Source)
            source_obj = Source(
                id=source_id,
                user_id=source_data.user_id,
                title=source_data.title,
                date=source_data.date,
                description=source_data.description,
                source_type=source_data.source_type,
            )

            result = db_manager.insert(
                obj=source_obj,
                session=session
            )

            if result:
                logger.info(f"Created new Source item with ID: {result.id}")
            else:
                logger.error(f"Failed to create new Source item: {result.title}")

            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to create source: {e}")
            raise
        finally:            
            if own_session:
                session.close()

    def update(
            self, 
            source_id: str, 
            source_data: SourceDict,
            session: Optional[Session] = None,
            as_dict: bool = False,
            include_relations: bool = True
        ) -> Source | dict:
        """Update an existing source by `source_id`.

        Returns the updated `SourceDict` on success or `None` if the source does not
        exist or the update fails.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()

        try:
            existing = db_manager.get_by_id(Source, source_id)
            if not existing:
                return None

            # Update fields
            existing.user_id = source_data.user_id
            existing.title = source_data.title
            existing.date = source_data.date
            existing.description = source_data.description
            existing.source_type = source_data.source_type

            modified = db_manager.modify(existing)
            return self._serialize(modified, as_dict, include_relations)
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to update source with ID {source_id}: {e}")
            raise
        finally:
            if own_session:
                session.close()

    def delete(
        self, 
        source_id: str,
        session: Optional[Session] = None
    ) -> bool:
        """Delete the source identified by `source_id`.

        Returns `True` when deletion succeeds, `False` otherwise.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()

        try:
            existing = db_manager.get_by_id(Source, source_id)
            if not existing:
                return False

            return db_manager.delete(existing)
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to delete source with ID {source_id}: {e}")
            raise
        finally:
            if own_session:
                session.close()

    def add_source_to_element(
        self,
        source_id: str,
        element_id: str,
        session: Optional[Session] = None
    ) -> bool:
        """Associate a source with an element.

        Uses ORM relationships through `db_manager` rather than raw SQL.
        A source can be associated with any element type regardless of source_type.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()
        
        try:
            source_obj = db_manager.get_by_id(Source, source_id)
            if not source_obj:
                return False

            element_type = self._resolve_element_model(element_id)
            if not element_type:
                return False

            element_obj = db_manager.get_by_id(element_type, element_id)
            if not element_obj:
                return False

            # avoid duplicates
            if any(s.id == source_id for s in element_obj.sources):
                return True

            element_obj.sources.append(source_obj)
            modified = db_manager.modify(element_obj)
            return bool(modified)
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to add source {source_id} to element {element_id}: {e}")
            raise
        finally:
            if own_session:
                session.close()

    def remove_source_from_element(
        self,
        source_id: str,
        element_id: str,
        session: Optional[Session] = None
    ) -> bool:
        """Remove a source association from an element.

        Uses ORM relationships through `db_manager` rather than raw SQL.
        Returns `True` if association was removed, `False` if not found.
        """
        own_session = session is None
        if own_session:
            session = db_manager.get_session()

        try:
            source_obj = db_manager.get_by_id(Source, source_id)
            if not source_obj:
                return False

            element_type = self._resolve_element_model(element_id)
            if not element_type:
                return False

            element_obj = db_manager.get_by_id(element_type, element_id)
            if not element_obj:
                return False

            if not any(s.id == source_id for s in element_obj.sources):
                return False

            element_obj.sources = [source for source in element_obj.sources if source.id != source_id]
            modified = db_manager.modify(element_obj)
            return bool(modified)
        except Exception as e:
            if own_session:
                session.rollback()
            logger.error(f"Failed to remove source {source_id} from element {element_id}: {e}")
            raise
        finally:
            if own_session:
                session.close()