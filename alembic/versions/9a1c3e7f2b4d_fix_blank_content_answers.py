"""fix blank exercise content answers

The previous migration (2f7a6c1d9b3e) derived each blank's answer by
diffing the filled `answer` string against `question`, assuming `answer`
was a full sentence. In practice `answer` for these types is `__`-joined
per-blank values (same convention as `matching`/`organize`), so the diff
produced empty answers. Re-derive `content.blanks` with a plain split.

Revision ID: 9a1c3e7f2b4d
Revises: 2f7a6c1d9b3e
Create Date: 2026-07-12 00:00:01.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '9a1c3e7f2b4d'
down_revision: Union[str, Sequence[str], None] = '2f7a6c1d9b3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_BLANK_TYPES = ('type_in_the_blank', 'select_in_the_blank')


def upgrade() -> None:
    import json as _json

    bind = op.get_bind()
    rows = bind.execute(
        sa.text(
            "SELECT id, answer, content FROM exercise "
            "WHERE exercise_type IN :types AND content IS NOT NULL"
        ).bindparams(sa.bindparam('types', expanding=True)),
        {"types": list(_BLANK_TYPES)},
    ).fetchall()

    for row_id, answer, content in rows:
        answers = [a.strip() for a in (answer or "").split('__')]
        blanks = content.get("blanks", [])
        if len(answers) != len(blanks):
            print(f"[fix_blank_content_answers] skipped exercise id={row_id!r}: "
                  f"{len(answers)} answers vs {len(blanks)} blanks")
            continue
        for blank, ans in zip(blanks, answers):
            blank["answer"] = ans
        bind.execute(
            sa.text("UPDATE exercise SET content = :content WHERE id = :id"),
            {"content": _json.dumps(content), "id": row_id},
        )


def downgrade() -> None:
    # Data-only fix; no schema change to revert.
    pass
