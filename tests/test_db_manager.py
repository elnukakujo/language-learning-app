"""Behavioral safety net for db_manager CRUD + transaction ownership.

Locks the contract the Phase 1 session-scope refactor must preserve:
- CRUD round-trips persist and retrieve.
- A caller-owned session commits ONCE for the whole unit of work (cascade),
  and rolls the whole thing back on error (no partial writes).
"""
from lapp.core.database import db_manager
from lapp.models.system_data import User


def test_insert_find_modify_delete_roundtrip(db):
    u = User(id="user_T1", username="alice")
    assert db.insert(u) is not None

    found = db.find_by_attr(model_class=User, attr_values={"id": "user_T1"})
    assert found is not None and found.username == "alice"

    found.username = "alice2"
    assert db.modify(found) is not None
    assert db.find_by_attr(model_class=User, attr_values={"id": "user_T1"}).username == "alice2"

    assert db.delete(found) is True
    assert db.find_by_attr(model_class=User, attr_values={"id": "user_T1"}) is None


def test_session_scope_commits_once(db):
    """Multiple deferred writes in one scope persist as a unit on exit."""
    with db.session_scope() as session:
        db.insert(User(id="user_T2", username="bob"), session=session, commit=False)
        db.insert(User(id="user_T3", username="carol"), session=session, commit=False)

    # both rows are visible from a fresh session
    assert db.find_by_attr(model_class=User, attr_values={"id": "user_T2"}) is not None
    assert db.find_by_attr(model_class=User, attr_values={"id": "user_T3"}) is not None


def test_session_scope_rolls_back_on_error(db):
    """A failing unit of work leaves no partial rows behind."""
    try:
        with db.session_scope() as session:
            db.insert(User(id="user_T4", username="dave"), session=session, commit=False)
            raise RuntimeError("boom")
    except RuntimeError:
        pass

    assert db.find_by_attr(model_class=User, attr_values={"id": "user_T4"}) is None
