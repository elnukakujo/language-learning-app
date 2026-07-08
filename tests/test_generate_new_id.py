"""Atomicity + legacy-seed correctness for db_manager.generate_new_id.

Locks in the Phase 3 contract: no duplicate IDs under concurrent generation,
and numbering continues from the highest existing legacy ID instead of
colliding with it.
"""
import threading

from lapp.core.database import db_manager
from lapp.models.system_data import User


def test_sequential_ids_increment(db):
    first = db.generate_new_id(User)
    second = db.generate_new_id(User)
    assert first == "user_U1"
    assert second == "user_U2"


def test_seeds_from_legacy_max_id(db):
    """A pre-existing row with a hand-set ID must not be collided with."""
    with db.session_scope() as s:
        db.insert(User(id="user_U7", username="legacy"), session=s, commit=False)

    next_id = db.generate_new_id(User)
    assert next_id == "user_U8"


def test_concurrent_generation_has_no_duplicates(db):
    """20 threads racing generate_new_id must all get distinct IDs."""
    ids: list[str] = []
    lock = threading.Lock()
    errors = []

    def worker():
        try:
            new_id = db.generate_new_id(User)
            with lock:
                ids.append(new_id)
        except Exception as e:  # pragma: no cover - surfaced via assertion below
            with lock:
                errors.append(e)

    threads = [threading.Thread(target=worker) for _ in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors, f"generate_new_id raised under concurrency: {errors}"
    assert len(ids) == len(set(ids)) == 20


if __name__ == "__main__":
    print("run via: uv run pytest tests/test_generate_new_id.py")
