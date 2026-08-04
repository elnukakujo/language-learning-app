"""Mutation counter contract: counts committed session_scope()s, not failed ones."""
from lapp.core.database import get_mutation_count, reset_mutation_counter
from lapp.models.system_data import User


def test_counter_increments_per_committed_scope(db):
    assert get_mutation_count() == 0
    with db.session_scope() as s:
        db.insert(User(id="user_C1", username="a"), session=s, commit=False)
    assert get_mutation_count() == 1
    with db.session_scope() as s:
        db.insert(User(id="user_C2", username="b"), session=s, commit=False)
    assert get_mutation_count() == 2


def test_counter_not_incremented_on_rollback(db):
    try:
        with db.session_scope() as s:
            db.insert(User(id="user_C3", username="c"), session=s, commit=False)
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    assert get_mutation_count() == 0


def test_reset_mutation_counter(db):
    with db.session_scope() as s:
        db.insert(User(id="user_C4", username="d"), session=s, commit=False)
    assert get_mutation_count() == 1
    reset_mutation_counter()
    assert get_mutation_count() == 0
