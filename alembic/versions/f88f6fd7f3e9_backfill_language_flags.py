"""backfill language flags from name

Revision ID: f88f6fd7f3e9
Revises: 4a4c0334263b
Create Date: 2026-08-08 21:02:45.719078

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f88f6fd7f3e9'
down_revision: Union[str, Sequence[str], None] = '4a4c0334263b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Mirrors client/src/utils/language_iso639.tsx LANGUAGE_FLAGS
_FLAGS_BY_NAME: dict[str, str] = {
    "Catalan": "🇪🇸",
    "Chinese": "🇨🇳",
    "Croatian": "🇭🇷",
    "Danish": "🇩🇰",
    "Dutch": "🇳🇱",
    "English": "🇬🇧",
    "Finnish": "🇫🇮",
    "French": "🇫🇷",
    "German": "🇩🇪",
    "Greek": "🇬🇷",
    "Italian": "🇮🇹",
    "Japanese": "🇯🇵",
    "Korean": "🇰🇷",
    "Lithuanian": "🇱🇹",
    "Macedonian": "🇲🇰",
    "Norwegian Bokmål": "🇳🇴",
    "Norwegian": "🇳🇴",
    "Polish": "🇵🇱",
    "Portuguese": "🇵🇹",
    "Romanian": "🇷🇴",
    "Russian": "🇷🇺",
    "Slovenian": "🇸🇮",
    "Spanish": "🇪🇸",
    "Swedish": "🇸🇪",
    "Ukrainian": "🇺🇦",
}


def upgrade() -> None:
    bind = op.get_bind()
    for name, flag in _FLAGS_BY_NAME.items():
        bind.execute(
            sa.text(
                "UPDATE language SET flag = :flag "
                "WHERE name = :name AND (flag IS NULL OR flag = '')"
            ),
            {"flag": flag, "name": name},
        )


def downgrade() -> None:
    # Data-only fix; no schema change to revert.
    pass
