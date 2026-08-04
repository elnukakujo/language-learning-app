"""Minimal self-check for the pure SRS helpers.

Run: `uv run python tests/test_helpers.py` (no pytest needed).
"""
from datetime import date, timedelta

from lapp.utils.helpers import (
    compute_recency_weight,
    update_difficulty,
    update_score,
)


def test_recency_weight_boosts_stale_items():
    today = date.today()
    fresh = compute_recency_weight(created_at=today - timedelta(days=10), last_seen_at=today)
    stale = compute_recency_weight(created_at=today - timedelta(days=10), last_seen_at=today - timedelta(days=9))
    assert stale > fresh  # longer since last seen → more forgetting → higher weight


def test_update_score_stays_in_bounds():
    today = date.today()
    perfect = update_score(score=50, last_seen_at=today - timedelta(days=3), similarity=1.0,
                           created_at=today - timedelta(days=3))
    wrong = update_score(score=50, last_seen_at=today - timedelta(days=3), similarity=0.0,
                         created_at=today - timedelta(days=3))
    assert 0.0 <= wrong <= perfect <= 100.0
    assert perfect > 50  # a correct review raises the score
    assert wrong < 50    # a wrong review lowers it


def test_update_difficulty_reacts_to_performance():
    today = date.today()
    kwargs = dict(last_seen_at=today - timedelta(days=2), previous_difficulty=0.5,
                  created_at=today - timedelta(days=2))
    easy = update_difficulty(new_score=95, **kwargs)
    hard = update_difficulty(new_score=10, **kwargs)
    assert hard > easy               # poor performance pushes difficulty up
    assert 0.0 <= easy <= 1.0 and 0.0 <= hard <= 1.0


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
    print("all helper checks passed")
