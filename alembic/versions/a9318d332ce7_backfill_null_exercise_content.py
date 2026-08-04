"""backfill exercise.content for rows still NULL

Migrations 2f7a6c1d9b3e/9a1c3e7f2b4d backfilled content once for the rows
that existed at the time. Exercises created afterward by an older/buggy
frontend or backend build can still end up with content=NULL for a
structured exercise_type (e.g. true_false with content=null crashes
practice/update pages). Re-run the same best-effort derivation from
question/answer for any row still missing it, so this self-heals on every
deploy instead of requiring a one-off manual fix.

Revision ID: a9318d332ce7
Revises: 9a1c3e7f2b4d
Create Date: 2026-07-14 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'a9318d332ce7'
down_revision: Union[str, Sequence[str], None] = '9a1c3e7f2b4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_STRUCTURED_TYPES = ('type_in_the_blank', 'select_in_the_blank', 'matching', 'organize', 'true_false')


def _parse_blank(question: str, answer: str) -> dict:
    # Mirrors client/src/components/exercises/typeInTheBlankExercise.tsx - answers are
    # '__'-joined per-blank values (see 9a1c3e7f2b4d), same convention as matching/organize.
    segments = question.split('__')
    answers = [a.strip() for a in answer.split('__')]
    blanks = [{"answer": a} for a in answers]
    return {"segments": segments, "blanks": blanks}


def _parse_matching(answer: str) -> dict:
    pairs = []
    for row in answer.split('\n'):
        cols = row.split('__')
        if len(cols) >= 2:
            pairs.append([cols[0], cols[1]])
    return {"pairs": pairs}


def _parse_organize(question: str) -> dict:
    items = question.split('__')
    return {"items": items, "answer_order": list(range(len(items)))}


def _parse_true_false(question: str, answer: str) -> dict:
    return {"statement": question, "answer": answer.strip().lower() == "true"}


def upgrade() -> None:
    import json as _json

    bind = op.get_bind()
    rows = bind.execute(
        sa.text(
            "SELECT id, exercise_type, question, answer FROM exercise "
            "WHERE exercise_type IN :types AND content IS NULL"
        ).bindparams(sa.bindparam('types', expanding=True)),
        {"types": list(_STRUCTURED_TYPES)},
    ).fetchall()

    for row_id, exercise_type, question, answer in rows:
        question = question or ""
        answer = answer or ""
        try:
            if exercise_type in ('type_in_the_blank', 'select_in_the_blank'):
                content = _parse_blank(question, answer)
            elif exercise_type == 'matching':
                content = _parse_matching(answer)
            elif exercise_type == 'organize':
                content = _parse_organize(question)
            elif exercise_type == 'true_false':
                content = _parse_true_false(question, answer)
            else:
                continue
        except Exception as exc:  # ponytail: best-effort migration, skip malformed rows
            print(f"[backfill_null_exercise_content] skipped exercise id={row_id!r} ({exercise_type}): {exc}")
            continue

        bind.execute(
            sa.text("UPDATE exercise SET content = :content WHERE id = :id"),
            {"content": _json.dumps(content), "id": row_id},
        )


def downgrade() -> None:
    # Data-only fix; no schema change to revert.
    pass
