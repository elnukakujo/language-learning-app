# src/lapp/core/database.py
import logging
from pathlib import Path
from typing import Optional, Type, TypeVar, Any

import sqlalchemy
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, scoped_session
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
    
    # ==================== CRUD Operations ====================
    
    def insert(self, obj: model_types, session: Optional[Session] = None) -> Optional[model_types]:
        """
        Insert a single object into the database.
        
        Args:
            obj: SQLAlchemy model instance to insert
            session: Optional session. If None, creates a new one.
        
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
            logger.info(f"Inserted {type(obj).__name__} with id: {obj.id}")
            return obj
        except IntegrityError as e:
            session.rollback()
            logger.warning(f"Insert failed due to integrity error: {e}")
            # Attempt to modify existing record
            return self.modify(obj, session)
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Insert failed: {e}")
            return None
        finally:
            if close_session:
                session.close()
    
    def insert_many(self, objs: list[model_types], session: Optional[Session] = None) -> bool:
        """
        Insert multiple objects into the database.
        
        Args:
            objs: List of SQLAlchemy model instances
            session: Optional session. If None, creates a new one.
        
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
            logger.info(f"Inserted {len(objs)} records")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Bulk insert failed: {e}")
            return False
        finally:
            if close_session:
                session.close()
    
    def modify(self, obj: model_types, session: Optional[Session] = None) -> Optional[model_types]:
        """
        Update an existing record or insert if not found.
        
        Uses SQLAlchemy's merge() which handles both update and insert.
        
        Args:
            obj: SQLAlchemy model instance
            session: Optional session. If None, creates a new one.
        
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
            logger.info(f"Modified {type(obj).__name__} with id: {obj.id}")
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
            # Find existing record by primary key
            existing = self.find_by_pk(obj, session)
            
            if not existing:
                logger.warning(f"Delete failed: Record not found")
                return False
            
            # Load relationships to trigger cascade deletions
            for rel in inspect(existing.__class__).relationships:
                getattr(existing, rel.key)
            
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
    
    def find_by_pk(self, obj: model_types, session: Optional[Session] = None) -> Optional[model_types]:
        """
        Find an existing record by primary key.
        
        Args:
            obj: Model instance containing primary key values
            session: Optional session. If None, creates a new one.
        
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
            
            # Query for existing record
            existing = session.query(model_class).filter_by(**pk_attrs).first()
            return existing
        finally:
            if close_session:
                session.close()
    
    def find_by_attr(
        self,
        model_class: Type[model_types],
        attr_values: dict[str, Any],
        session: Optional[Session] = None
    ) -> Optional[model_types]:
        """
        Find a record by specific attributes.
        
        Args:
            model_class: The SQLAlchemy model class to query
            attr_values: Dictionary of attribute names and values
            session: Optional session. If None, creates a new one.
        
        Returns:
            The matching record or None if not found
        """
        close_session = False
        if session is None:
            session = self.get_session()
            close_session = True
        
        try:
            existing = session.query(model_class).filter_by(**attr_values).first()
            
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
        session: Optional[Session] = None
    ) -> list[model_types]:
        """
        Find all records matching optional filters.
        
        Args:
            model_class: The SQLAlchemy model class to query
            filters: Optional dictionary of filter conditions
            session: Optional session. If None, creates a new one.
        
        Returns:
            List of matching records
        """
        close_session = False
        if session is None:
            session = self.get_session()
            close_session = True
        
        try:
            if not isinstance(model_class, list):
                model_class = list(model_class)
            
            results = []

            for model in model_class:
                query = session.query(model)
                
                if filters:
                    query = query.filter_by(**filters)
            
                results += query.all()
            return results
        finally:
            if close_session:
                session.close()
    
    def generate_new_id(
        self,
        model_class: Type[model_types],
        session: Optional[Session] = None,
        language_id: Optional[str] = None,
        unit_id: Optional[str] = None,
    ) -> str:
        """
        Generate a new sequential ID for any model type.
        
        ID Format:
        - Language: "lang_L{n}" (global scope)
        - Unit: "unit_U{n}" (scoped to language)
        - Vocabulary: "voc_V{n}" (scoped to unit)
        - Grammar: "gram_G{n}" (scoped to unit)
        - Character: "char_C{n}" (scoped to unit)
        - Exercise: "ex_E{n}" (scoped to unit)
        
        Args:
            model_class: The model class to generate ID for
            session: Optional session. If None, creates a new one.
            language_id: Required for Unit model
            unit_id: Required for Vocabulary, Grammar, Character, Exercise models
        
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
                "Language": {"prefix": "lang_L", "scope": None},
                "Unit": {"prefix": "unit_U", "scope": "language"},
                "Vocabulary": {"prefix": "voc_V", "scope": "unit"},
                "Grammar": {"prefix": "gram_G", "scope": "unit"},
                "Character": {"prefix": "char_C", "scope": "unit"},
                "Exercise": {"prefix": "ex_E", "scope": "unit"},
            }
            
            if model_class.__name__ not in id_config:
                raise ValueError(f"Unsupported model class: {model_class.__name__}")
            
            config = id_config[model_class.__name__]
            prefix = config["prefix"]
            scope = config["scope"]
            
            # Build query based on scope
            query = select(model_class.id)
            
            if scope == "language":
                if not language_id:
                    raise ValueError(f"{model_class.__name__} requires language_id")
                query = query.where(model_class.language_id == language_id)
            elif scope == "unit":
                if not unit_id:
                    raise ValueError(f"{model_class.__name__} requires unit_id")
                query = query.where(model_class.unit_id == unit_id)
            # else: global scope (no filter needed)
            
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