# src/lapp/core/database.py
import logging
from pathlib import Path
from typing import Optional, Type, TypeVar, Any

import sqlalchemy
from sqlalchemy import create_engine, select, union_all, literal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, scoped_session, selectinload
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import Flask

logger = logging.getLogger(__name__)

# Create base for models
Base = declarative_base()

# Type variable for model classes
model_types = TypeVar('T', bound="Base")

class DatabaseManager:
    """
    Manages database connections, sessions, and CRUD operations.
    
    This class provides a centralized interface for database operations,
    including initialization, session management, and common CRUD methods.
    """
    
    def __init__(self, database_uri: Optional[str] = None):
        """
        Initialize the DatabaseManager.
        
        Args:
            database_uri: SQLAlchemy database URI. If None, will be set later via init_app()
        """
        self.engine: Optional[sqlalchemy.engine.Engine] = None
        self.SessionLocal: Optional[sessionmaker] = None
        self._scoped_session: Optional[scoped_session] = None
        
        if database_uri:
            self._create_engine(database_uri)
    
    def _create_engine(self, database_uri: str) -> None:
        """Create SQLAlchemy engine and session factory."""
        self.engine = create_engine(
            database_uri,
            echo=False,  # Set to True for SQL debugging
            pool_pre_ping=True,  # Verify connections before using
        )
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False
        )
        self._scoped_session = scoped_session(self.SessionLocal)
    
    def init_app(self, app: Flask) -> None:
        """
        Initialize database with Flask app.
        
        Args:
            app: Flask application instance
        """
        database_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        
        if not database_uri:
            raise ValueError("SQLALCHEMY_DATABASE_URI not found in app config")
        
        # Ensure database directory exists
        if database_uri.startswith('sqlite:///'):
            db_path = Path(database_uri.replace('sqlite:///', ''))
            db_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Database path: {db_path}")
        
        self._create_engine(database_uri)
        
        # Register teardown to close sessions
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            self.close_session()
        
        logger.info("DatabaseManager initialized with Flask app")
    
    def create_tables(self) -> None:
        """Create all tables defined in models."""
        if not self.engine:
            raise RuntimeError("Database engine not initialized. Call init_app() first.")
        
        import lapp.models  # Ensure models are imported in the right order

        Base.metadata.create_all(self.engine)
        logger.info("Database tables created successfully")
    
    def drop_tables(self) -> None:
        """Drop all tables (use with caution!)."""
        if not self.engine:
            raise RuntimeError("Database engine not initialized")
        
        Base.metadata.drop_all(self.engine)
        logger.warning("All database tables dropped")
    
    def get_session(self) -> Session:
        """
        Get a new database session.
        
        Returns:
            Session: SQLAlchemy session instance
        """
        if not self._scoped_session:
            raise RuntimeError("Database not initialized. Call init_app() first.")
        
        return self._scoped_session()
    
    def close_session(self) -> None:
        """Close the current scoped session."""
        if self._scoped_session:
            self._scoped_session.remove()
    
    def _load_relationships(self, query, model_class: Type[model_types], load_relationships: bool = True):
        """
        Helper method to add relationship loading to a query.
        
        Args:
            query: SQLAlchemy query object
            model_class: The model class being queried
            load_relationships: Whether to load relationships
        
        Returns:
            Query with relationship loading options added
        """
        if not load_relationships:
            return query
        
        # Get all relationships for the model
        mapper = inspect(model_class)
        
        # Use selectinload for one-to-many relationships (more efficient for collections)
        for relationship in mapper.relationships:
            query = query.options(selectinload(getattr(model_class, relationship.key)))
        
        return query
    
    def _eager_load_object_relationships(self, obj: model_types, session: Session) -> None:
        """
        Eagerly load all relationships on an existing object.
        This ensures the object can be used even after the session closes.
        
        Args:
            obj: The object whose relationships should be loaded
            session: The session containing the object
        """
        mapper = inspect(type(obj))
        
        # Access each relationship to trigger loading while session is still open
        for relationship in mapper.relationships:
            try:
                # Access the relationship attribute to load it
                attr = getattr(obj, relationship.key)
                # If it's a list, access its length to ensure it's fully loaded
                if isinstance(attr, list):
                    len(attr)
            except Exception as e:
                logger.warning(f"Could not load relationship {relationship.key}: {e}")
    
    # ==================== CRUD Operations ====================
    
    def insert(self, obj: model_types, session: Optional[Session] = None, load_relationships: bool = True) -> Optional[model_types]:
        """
        Insert a single object into the database.
        
        Args:
            obj: SQLAlchemy model instance to insert
            session: Optional session. If None, creates a new one.
            load_relationships: If True, eagerly load all relationships before closing session
        
        Returns:
            The inserted object, or None if failed
        """
        close_session = False
        if session is None:
            session = self.get_session()
            close_session = True
        
        try:
            session.add(obj)
            session.commit()
            session.refresh(obj)  # Refresh to get generated IDs
            
            # Load all relationships before closing the session
            if load_relationships:
                self._eager_load_object_relationships(obj, session)
            
            logger.info(f"Inserted {type(obj).__name__} with id: {obj.id}")
            return obj
        except IntegrityError as e:
            session.rollback()
            logger.warning(f"Insert failed due to integrity error: {e}")
            # Attempt to modify existing record
            return self.modify(obj, session, load_relationships)
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Insert failed: {e}")
            return None
        finally:
            if close_session:
                session.close()
    
    def insert_many(self, objs: list[model_types], session: Optional[Session] = None, load_relationships: bool = True) -> bool:
        """
        Insert multiple objects into the database.
        
        Args:
            objs: List of SQLAlchemy model instances
            session: Optional session. If None, creates a new one.
            load_relationships: If True, eagerly load all relationships before closing session
        
        Returns:
            True if all inserts succeeded, False otherwise
        """
        close_session = False
        if session is None:
            session = self.get_session()
            close_session = True
        
        try:
            session.add_all(objs)
            session.commit()
            for obj in objs:
                session.refresh(obj)
                # Load all relationships before closing the session
                if load_relationships:
                    self._eager_load_object_relationships(obj, session)
            logger.info(f"Inserted {len(objs)} records")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Bulk insert failed: {e}")
            return False
        finally:
            if close_session:
                session.close()
    
    def modify(self, obj: model_types, session: Optional[Session] = None, load_relationships: bool = True) -> Optional[model_types]:
        """
        Update an existing record or insert if not found.
        
        Uses SQLAlchemy's merge() which handles both update and insert.
        
        Args:
            obj: SQLAlchemy model instance
            session: Optional session. If None, creates a new one.
            load_relationships: If True, eagerly load all relationships before closing session
        
        Returns:
            The merged object, or None if failed
        """
        close_session = False
        if session is None:
            session = self.get_session()
            close_session = True
        
        try:
            merged_obj = session.merge(obj)
            session.commit()
            session.refresh(merged_obj)
            
            # Load all relationships before closing the session
            if load_relationships:
                self._eager_load_object_relationships(merged_obj, session)
            
            logger.info(f"Modified {type(merged_obj).__name__} with id: {merged_obj.id}")
            return merged_obj
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Modify failed: {e}")
            return None
        finally:
            if close_session:
                session.close()
    
    def delete(self, obj: model_types, session: Optional[Session] = None) -> bool:
        """
        Delete a record from the database.
        
        Args:
            obj: SQLAlchemy model instance to delete
            session: Optional session. If None, creates a new one.
        
        Returns:
            True if deletion succeeded, False otherwise
        """
        close_session = False
        if session is None:
            session = self.get_session()
            close_session = True
        
        try:
            # Find existing record by primary key with relationships loaded
            existing = self.find_by_pk(obj, session, load_relationships=True)
            
            if not existing:
                logger.warning(f"Delete failed: Record not found")
                return False
            
            session.delete(existing)
            session.commit()
            logger.info(f"Deleted {type(obj).__name__} with id: {obj.id}")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Delete failed: {e}")
            return False
        finally:
            if close_session:
                session.close()
    
    def find_by_pk(
        self, 
        obj: model_types, 
        session: Optional[Session] = None,
        load_relationships: bool = True
    ) -> Optional[model_types]:
        """
        Find an existing record by primary key.
        
        Args:
            obj: Model instance containing primary key values
            session: Optional session. If None, creates a new one.
            load_relationships: If True, eagerly load all relationships
        
        Returns:
            Existing record or None if not found
        """
        close_session = False
        if session is None:
            session = self.get_session()
            close_session = True
        
        try:
            model_class = type(obj)
            mapper = inspect(model_class)
            
            # Extract primary key values
            pk_attrs = {key.name: getattr(obj, key.name) for key in mapper.primary_key}
            
            # Build query
            query = session.query(model_class).filter_by(**pk_attrs)
            
            # Add relationship loading
            query = self._load_relationships(query, model_class, load_relationships)
            
            existing = query.first()
            return existing
        finally:
            if close_session:
                session.close()
    
    def find_by_attr(
        self,
        model_class: Type[model_types],
        attr_values: dict[str, Any],
        session: Optional[Session] = None,
        load_relationships: bool = True
    ) -> Optional[model_types]:
        """
        Find a record by specific attributes.
        
        Args:
            model_class: The SQLAlchemy model class to query
            attr_values: Dictionary of attribute names and values
            session: Optional session. If None, creates a new one.
            load_relationships: If True, eagerly load all relationships
        
        Returns:
            The matching record or None if not found
        """
        close_session = False
        if session is None:
            session = self.get_session()
            close_session = True
        
        try:
            query = session.query(model_class).filter_by(**attr_values)
            
            # Add relationship loading
            query = self._load_relationships(query, model_class, load_relationships)
            
            existing = query.first()
            
            if existing:
                return existing
            else:
                logger.warning(f"No {model_class.__name__} found with attributes: {attr_values}")
                return None
        finally:
            if close_session:
                session.close()
    
    def find_all(
        self,
        model_class: Type[model_types] | list[Type[model_types]],
        filters: Optional[dict[str, Any]] = None,
        session: Optional[Session] = None,
        load_relationships: bool = True
    ) -> list[model_types]:
        """
        Find all records matching optional filters.
        
        Args:
            model_class: The SQLAlchemy model class to query (or list of classes)
            filters: Optional dictionary of filter conditions
            session: Optional session. If None, creates a new one.
            load_relationships: If True, eagerly load all relationships
        
        Returns:
            List of matching records
        """
        close_session = False
        if session is None:
            session = self.get_session()
            close_session = True
        
        try:
            if not isinstance(model_class, list):
                model_class = [model_class]
            
            results = []

            for model in model_class:
                query = session.query(model)
                
                if filters:
                    query = query.filter_by(**filters)
                
                # Add relationship loading
                query = self._load_relationships(query, model, load_relationships)
            
                results += query.all()
            return results
        finally:
            if close_session:
                session.close()
    
    def get_by_id(
        self,
        model_class: Type[model_types],
        id_value: Any,
        session: Optional[Session] = None,
        load_relationships: bool = True
    ) -> Optional[model_types]:
        """
        Convenience method to get a record by its ID.
        
        Args:
            model_class: The SQLAlchemy model class to query
            id_value: The ID value to search for
            session: Optional session. If None, creates a new one.
            load_relationships: If True, eagerly load all relationships
        
        Returns:
            The matching record or None if not found
        """
        return self.find_by_attr(
            model_class, 
            {"id": id_value}, 
            session, 
            load_relationships
        )
    
    def generate_new_id(
        self,
        model_class: Type[model_types],
        session: Optional[Session] = None,
    ) -> str:
        """
        Generate a new sequential ID for any model type.
        
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
        - User: "user_U{n}"
        - UserPreferences: "pref_P{n}"
        - Source: "src_S{n}"
        - Tag: "tag_T{n}"
        - StrengthsAndWeaknesses: "sw_S{n}"
        - ProgressTracking: "pt_P{n}"
        
        Args:
            model_class: The model class to generate ID for
            session: Optional session. If None, creates a new one.
        
        Returns:
            New ID string (e.g., "voc_V42")
        
        Raises:
            ValueError: If required scope parameters are missing
        """
        close_session = False
        if session is None:
            session = self.get_session()
            close_session = True
        
        try:
            # Define ID prefixes and letters for each model
            id_config = {
                "Language": "lang_L",
                "Lesson": "lesson_L",
                "Vocabulary": "voc_V",
                "Grammar": "gram_G",
                "Calligraphy": "call_C",
                "Exercise": "ex_E",
                "Character": "char_C",
                "Word": "word_W",
                "Passage": "pass_P",
                "User": "user_U",
                "UserPreferences": "pref_P",
                "Source": "src_S",
                "Tag": "tag_T",
                "StrengthsAndWeaknesses": "sw_S",
                "ProgressTracking": "pt_P"
            }
            
            if model_class.__name__ not in id_config:
                raise ValueError(f"Unsupported model class: {model_class.__name__}")
            
            prefix = id_config[model_class.__name__]
            
            # Build query based on scope
            query = select(model_class.id)
            
            # Get all existing IDs
            existing_ids = session.scalars(query).all()
            
            # Extract numeric parts
            numbers = []
            for id_str in existing_ids:
                try:
                    # Split by underscore and get the part after the letter
                    # e.g., "voc_V42" -> ["voc", "V42"] -> "42"
                    num_part = id_str.split("_")[-1][1:]  # Remove the letter prefix
                    num = int(num_part)
                    numbers.append(num)
                except (ValueError, IndexError):
                    continue
            
            # Generate next number
            next_num = max(numbers) + 1 if numbers else 1
            
            # Return formatted ID
            return f"{prefix}{next_num}"
            
        finally:
            if close_session:
                session.close()

    def search_elements(self, user_id: str, query: str) -> list[dict[str, Any]]:
        """
        Search across containers, features, and components for a user.

        Args:
            user_id: The owner user ID used to scope search results.
            query: Free-text query string.

        Returns:
            Flat list of {category, type, id, label} dictionaries.
        """
        normalized_query = (query or "").strip()
        if len(normalized_query) < 2:
            return []

        session = self.get_session()
        try:
            from ..models.containers import Language, Lesson
            from ..models.features import Vocabulary, Grammar, Calligraphy, Exercise
            from ..models.components import Character, Word, Passage

            query_pattern = f"%{normalized_query}%"

            language_query = select(
                literal("container").label("category"),
                literal("language").label("type"),
                Language.id.label("id"),
                Language.name.label("label"),
            ).where(
                Language.user_id == user_id,
                Language.name.is_not(None),
                Language.name.ilike(query_pattern),
            )

            lesson_query = select(
                literal("container").label("category"),
                literal("lesson").label("type"),
                Lesson.id.label("id"),
                Lesson.title.label("label"),
            ).where(
                Lesson.user_id == user_id,
                Lesson.title.is_not(None),
                Lesson.title.ilike(query_pattern),
            )

            vocabulary_query = select(
                literal("feature").label("category"),
                literal("vocabulary").label("type"),
                Vocabulary.id.label("id"),
                Word.word.label("label"),
            ).join(Word, Word.id == Vocabulary.word_id).join(
                Lesson, Lesson.id == Vocabulary.lesson_id
            ).where(
                Lesson.user_id == user_id,
                Word.word.is_not(None),
                Word.word.ilike(query_pattern),
            )

            grammar_query = select(
                literal("feature").label("category"),
                literal("grammar").label("type"),
                Grammar.id.label("id"),
                Grammar.title.label("label"),
            ).join(Lesson, Lesson.id == Grammar.lesson_id).where(
                Lesson.user_id == user_id,
                Grammar.title.is_not(None),
                Grammar.title.ilike(query_pattern),
            )

            calligraphy_query = select(
                literal("feature").label("category"),
                literal("calligraphy").label("type"),
                Calligraphy.id.label("id"),
                Character.character.label("label"),
            ).join(Character, Character.id == Calligraphy.character_id).join(
                Lesson, Lesson.id == Calligraphy.lesson_id
            ).where(
                Lesson.user_id == user_id,
                Character.character.is_not(None),
                Character.character.ilike(query_pattern),
            )

            exercise_query = select(
                literal("feature").label("category"),
                literal("exercise").label("type"),
                Exercise.id.label("id"),
                Exercise.question.label("label"),
            ).join(Lesson, Lesson.id == Exercise.lesson_id).where(
                Lesson.user_id == user_id,
                Exercise.question.is_not(None),
                Exercise.question.ilike(query_pattern),
            )

            character_query = select(
                literal("component").label("category"),
                literal("character").label("type"),
                Character.id.label("id"),
                Character.character.label("label"),
            ).join(Language, Language.id == Character.language_id).where(
                Language.user_id == user_id,
                Character.character.is_not(None),
                Character.character.ilike(query_pattern),
            )

            word_query = select(
                literal("component").label("category"),
                literal("word").label("type"),
                Word.id.label("id"),
                Word.word.label("label"),
            ).join(Language, Language.id == Word.language_id).where(
                Language.user_id == user_id,
                Word.word.is_not(None),
                Word.word.ilike(query_pattern),
            )

            passage_query = select(
                literal("component").label("category"),
                literal("passage").label("type"),
                Passage.id.label("id"),
                Passage.text.label("label"),
            ).join(Language, Language.id == Passage.language_id).where(
                Language.user_id == user_id,
                Passage.text.is_not(None),
                Passage.text.ilike(query_pattern),
            )

            union_query = union_all(
                language_query,
                lesson_query,
                vocabulary_query,
                grammar_query,
                calligraphy_query,
                exercise_query,
                character_query,
                word_query,
                passage_query,
            ).subquery()

            statement = select(
                union_query.c.category,
                union_query.c.type,
                union_query.c.id,
                union_query.c.label,
            ).order_by(union_query.c.label).limit(20)

            rows = session.execute(statement).mappings().all()
            return [
                {
                    "category": row["category"],
                    "type": row["type"],
                    "id": row["id"],
                    "label": row["label"],
                }
                for row in rows
            ]
        finally:
            session.close()


# Global instance
db_manager = DatabaseManager()

# Convenience function for Flask initialization
def init_db(app: Flask) -> DatabaseManager:
    """
    Initialize database with Flask app.
    
    Args:
        app: Flask application instance
    
    Returns:
        DatabaseManager instance
    """
    db_manager.init_app(app)
    db_manager.create_tables()
    return db_manager