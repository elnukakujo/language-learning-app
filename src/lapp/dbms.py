from pyexpat import model
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pathlib import Path

import os
import logging
logger = logging.getLogger(__name__)

Base = declarative_base()

def init_db(language_name: str) -> tuple[sqlalchemy.engine.Engine, sqlalchemy.orm.session.Session]:
    """
    Initializes the SQLite database for the given language.

    If the database file already exists, this will log that the existing database is found.
    Otherwise, it creates a new database and logs its creation. The function then creates all
    the tables defined by the SQLAlchemy Base metadata.

    Args:
        language_name (str): The name of the language used to name the database file.

    Returns:
        tuple: A tuple containing the created SQLAlchemy Engine and Session.
    """
    db_path = Path(__file__).resolve().parent.parent.parent / "db" / f"{language_name}.db"

    if db_path.exists():
        logger.info(f"Found existing database {db_path.name}.")
    else:
        logger.info(f"Creating new database {db_path.name}.")

    DATABASE_URL = f"sqlite:///{db_path}"  # Absolute path

    engine = create_engine(DATABASE_URL, echo=True)
    session = sessionmaker(bind=engine)
    session = session()

    Base.metadata.create_all(engine)
    logger.info(f"Database {language_name}.db initialized successfully.")

    return engine, session

def inserts(session: Session, objs: list[sqlalchemy.orm.decl_api.DeclarativeMeta]) -> None:
    """
    Inserts multiple objects into the database within a given session.

    Iterates over each object in the list and inserts it individually using the insert() function.

    Args:
        session (Session): The SQLAlchemy session used for database operations.
        objs (list): A list of SQLAlchemy model instances to insert.
    
    Returns:
        None
    """
    for obj in objs:
        insert(session, obj)

def insert(session: Session, obj: sqlalchemy.orm.decl_api.DeclarativeMeta) -> None:
    """
    Inserts a single object into the database.

    Attempts to add and commit the object to the session. If an IntegrityError or other SQLAlchemyError
    occurs, it logs a warning, rolls back the session and attempts to modify the existing record instead.

    Args:
        session (Session): The SQLAlchemy session to use for the operation.
        obj (DeclarativeMeta): The model instance to insert.

    Returns:
        None
    """
    try:
        session.add(obj)
        session.commit()
    except (SQLAlchemyError, IntegrityError) as e:
        logger.warning(f"Insert failed: {e}. Attempting to modify an existing record.")
        session.rollback()
        modify(session, obj)  # Attempt to modify if insert fails

def find_by_pk(session: Session, obj: sqlalchemy.orm.decl_api.DeclarativeMeta) -> tuple[sqlalchemy.orm.decl_api.DeclarativeMeta, sqlalchemy.orm.Mapper, dict]:
    """
    Finds an existing record based on the primary key(s) of the provided object.

    Inspects the model to extract the primary key attributes, then queries the database for a matching record.
    If found, returns the record along with its mapper and the primary key attribute values.

    Args:
        session (Session): The SQLAlchemy session used for querying.
        obj (DeclarativeMeta): The instance containing primary key values.

    Returns:
        tuple: A tuple containing the existing record, its mapper, and a dictionary of primary key attributes.
                If no record is found, logs a warning and returns None.
    """
    model_class = type(obj)
    mapper = inspect(model_class)

    # Get the unique/primary key attributes
    pk_attrs = {key.name: getattr(obj, key.name) for key in mapper.primary_key}

    # Query for the existing row
    existing = session.query(model_class).filter_by(**pk_attrs).first()
    
    if existing:
        return existing, mapper, pk_attrs
    else:
        logger.warning("No record found with matching unique attributes.")
        return None, None, None

def modify(session: Session, obj: sqlalchemy.orm.decl_api.DeclarativeMeta) -> sqlalchemy.orm.decl_api.DeclarativeMeta:
    """
    Modifies an existing database record or adds a new one using the provided SQLAlchemy session and object.

    This function first attempts to locate an existing record in the database that matches the primary key of the given object.
    If a matching record is found, it iterates over all attributes of the object's mapped columns (excluding primary key attributes)
    and for each attribute that is explicitly set on the new object and not None, update the existing record if the values differ.
    If no matching record is found, the object is added as a new record.

    After applying the changes, the function attempts to commit the transaction. 
    If an error occurs during commit (SQLAlchemyError), the transaction is rolled back and the error is logged.

    Args:
        session (Session): The SQLAlchemy session used to interact with the database.
        obj (DeclarativeMeta): The SQLAlchemy declarative model instance representing the record to modify or insert.

    Returns:
        Updated Object (DeclarativeMeta): The modified or newly created object after the commit.
    
    Raises:
        SQLAlchemyError: If the commit fails, the exception is caught, and an error message is logged after rolling back the session.
    """
    # Try to find existing row
    existing_data = find_by_pk(session, obj)

    if existing_data:
        existing, mapper, pk_attrs = existing_data
        for attr in mapper.attrs.keys():
            if attr in pk_attrs:
                continue  # Don't update primary key

            # Skip if new object doesn't explicitly set this attribute
            if not hasattr(obj, attr):
                continue

            new_value = getattr(obj, attr)
            if new_value is None:
                continue  # Treat None as "not provided", skip

            current_value = getattr(existing, attr)
            if current_value != new_value:
                setattr(existing, attr, new_value)
        session.commit()
        return existing
    else:
        session.add(obj)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error committing modify: {e}")
            return None
        return obj

def delete(session: Session, obj: sqlalchemy.orm.decl_api.DeclarativeMeta) -> None:
    """
    Deletes an existing record from the database.

    Attempts to find the record based on the object's primary key.
    If found, deletes the record and commits the session.
    Logs a warning if the record cannot be found, and logs an error if the commit fails.

    Args:
        session (Session): The SQLAlchemy session used for the operation.
        obj (DeclarativeMeta): The instance whose corresponding record is to be deleted.

    Returns:
        None
    """
    result = find_by_pk(session, obj)

    if result:
        existing, _, _ = result
        try:
            session.delete(existing)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Delete failed: {e}")
    else:
        logger.warning("Delete failed: No record found with matching unique attributes.")

def find_by_attr(session: Session, attr_values: dict, model_class: sqlalchemy.orm.decl_api.DeclarativeMeta) -> dict:
    """
    Finds a record by specific attribute values.

    Given a dictionary of attribute names and values and a model class, queries the database for a record
    that matches all the provided attributes. If a matching record is found, returns a dictionary
    with the record's column names and values (excluding any private attributes).

    Args:
        session (Session): The SQLAlchemy session used for querying.
        attr_values (dict): A dictionary of column names and their respective values to filter by.
        model_class (DeclarativeMeta): The SQLAlchemy declarative model class to query.

    Returns:
        dict: A dictionary of attributes and values for the found record, or None if no record matches.
    
    Raises:
        ValueError: If no model_class is provided.
    """
    if not model_class:
        raise ValueError("Model class must be provided.")

    # Query for the existing row
    existing = session.query(model_class).filter_by(**attr_values).first()

    if existing:
        return {k: v for k, v in existing.__dict__.items() if not k.startswith('_')}
    else:
        logger.warning("No record found with matching attributes.")
        return None