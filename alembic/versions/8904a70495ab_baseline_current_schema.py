"""baseline: current schema

Revision ID: 8904a70495ab
Revises:
Create Date: 2026-07-08 21:36:39.582617

Intentional no-op. Existing databases were built by create_all()/hand-written
SQL (docs/migrations/); this revision is the marker every such DB gets
`alembic stamp`ed to so future `alembic upgrade head` calls apply only new,
real changes on top. Brand-new databases are bootstrapped via create_all()
and stamped here too (see DatabaseManager.init_app) rather than replaying
this no-op — don't add real DDL to upgrade()/downgrade() here.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8904a70495ab'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
