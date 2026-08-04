"""add days_active_last_counted_at column

Revision ID: b1e4a6f930cd
Revises: a9318d332ce7
Create Date: 2026-07-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b1e4a6f930cd'
down_revision: Union[str, Sequence[str], None] = 'a9318d332ce7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'commitment_log',
        sa.Column('days_active_last_counted_at', sa.String(), nullable=False, server_default=''),
    )
    op.alter_column('commitment_log', 'days_active_last_counted_at', server_default=None)


def downgrade() -> None:
    op.drop_column('commitment_log', 'days_active_last_counted_at')
