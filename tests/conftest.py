"""Shared test fixtures: a Flask app on a throwaway SQLite DB with fresh tables.

"""
import pytest

from lapp.api.app import create_app
from lapp.core.database import db_manager


@pytest.fixture(scope="session")
def app():
    app = create_app(config_name="test")
    return app


@pytest.fixture()
def db(app):
    """Fresh schema for each test; yields the db_manager singleton."""
    with app.app_context():
        db_manager.drop_tables()
        db_manager.create_tables()
        yield db_manager
        db_manager.close_session()
