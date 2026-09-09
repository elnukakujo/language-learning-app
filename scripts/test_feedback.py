#!/usr/bin/env python3
"""Smoke-test AI feedback against the configured text-gen endpoint.

Runs the full FeedbackService.generate_feedback flow on a real exercise and
reports whether the model produced feedback or fell back to the hardcoded
template. Exits non-zero on fallback so it can be used in a script/CI.

Usage:
    uv run python scripts/test_feedback.py            # prod schema
    uv run python scripts/test_feedback.py --env dev
"""

import argparse
import time

from flask import Flask

from config import config as CONFIGS
from lapp.core.database import db_manager
from lapp.models import Exercise
from lapp.services.feedback import FeedbackService


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-test AI feedback generation.")
    parser.add_argument("--env", default="prod", choices=["dev", "test", "prod"])
    args = parser.parse_args()

    app = Flask(__name__)
    app.config.from_object(CONFIGS[args.env])
    db_manager.init_app(app)

    svc = FeedbackService()
    results = {"score": 0.4, "similarity": 0.4}
    threshold = 0.75
    source_lang = "eng"

    with app.app_context():
        with db_manager.session_scope() as session:
            exercise = session.query(Exercise).first()
            if not exercise:
                print("FAIL: no exercise found — seed the DB first (scripts/seed_demo.py)")
                return 1

            ex_id = exercise.id
            ex_type = exercise.exercise_type

            t0 = time.time()
            fb = svc.generate_feedback(
                ex_id=ex_id,
                user_input="wrong answer",
                input_type="text",
                target_lang_code="jpn",
                source_lang_code=source_lang,
                results=results,
                threshold=threshold,
                session=session,
            )
            elapsed = time.time() - t0

    fallback = svc._fallback_feedback({
        "score": results["score"],
        "correct": results["score"] > threshold,
        "exercise_type": ex_type,
        "source_lang_code": source_lang,
    })

    if not fb or fb == fallback:
        print(f"FAIL: AI feedback fell back to the template ({elapsed:.1f}s)")
        print(f"  exercise: {ex_id} ({ex_type})")
        print(f"  got: {fb!r}")
        return 1

    print(f"PASS: AI feedback generated in {elapsed:.1f}s")
    print(f"  exercise: {ex_id} ({ex_type})")
    print(f"  feedback: {fb}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
