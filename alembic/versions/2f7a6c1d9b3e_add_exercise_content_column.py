"""add exercise content column

Revision ID: 2f7a6c1d9b3e
Revises: 018c6b4ce3e1
Create Date: 2026-07-12 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2f7a6c1d9b3e'
down_revision: Union[str, Sequence[str], None] = '018c6b4ce3e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Exercise types whose question/answer strings get parsed into `content`.
_STRUCTURED_TYPES = ('type_in_the_blank', 'select_in_the_blank', 'matching', 'organize', 'true_false')


def _parse_blank(question: str, answer: str) -> dict:
    # Mirrors client/src/components/exercises/typeInTheBlankExercise.tsx
    parts = question.split('__')
    blanks = []
    for i in range(len(parts) - 1):
        part = parts[i]
        next_part = parts[i + 1] if i + 1 < len(parts) else ""
        start = answer.find(part) + len(part)
        end = answer.find(next_part, start) if next_part else len(answer)
        ans = "" if (start < len(part) or end < start) else answer[start:end].strip()
        blanks.append({"answer": ans})
    return {"segments": parts, "blanks": blanks}


def _parse_matching(answer: str) -> dict:
    # Mirrors client/src/components/exercises/matchingExercise.tsx
    pairs = []
    for row in answer.split('\n'):
        cols = row.split('__')
        if len(cols) >= 2:
            pairs.append([cols[0], cols[1]])
    return {"pairs": pairs}


def _parse_organize(question: str) -> dict:
    # Mirrors client/src/components/exercises/organizeExercise.tsx
    # (question order is itself the correct order; frontend shuffles it for display)
    items = question.split('__')
    return {"items": items, "answer_order": list(range(len(items)))}


def _parse_true_false(question: str, answer: str) -> dict:
    # Mirrors client/src/components/exercises/trueFalseExercise.tsx
    return {"statement": question, "answer": answer.strip().lower() == "true"}


def upgrade() -> None:
    op.add_column('exercise', sa.Column('content', sa.JSON(), nullable=True))

    bind = op.get_bind()
    rows = bind.execute(
        sa.text(
            "SELECT id, exercise_type, question, answer FROM exercise "
            "WHERE exercise_type IN :types"
        ).bindparams(sa.bindparam('types', expanding=True)),
        {"types": list(_STRUCTURED_TYPES)},
    ).fetchall()

    import json as _json

    for row in rows:
        row_id, exercise_type, question, answer = row
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
            print(f"[add_exercise_content_column] skipped exercise id={row_id!r} ({exercise_type}): {exc}")
            continue

        bind.execute(
            sa.text("UPDATE exercise SET content = :content WHERE id = :id"),
            {"content": _json.dumps(content), "id": row_id},
        )


def downgrade() -> None:
    op.drop_column('exercise', 'content')
