"""add id_counter table for atomic ID generation

Revision ID: 1ed43cbdcb5d
Revises: 8904a70495ab
Create Date: 2026-07-08 21:47:17.626359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ed43cbdcb5d'
down_revision: Union[str, Sequence[str], None] = '8904a70495ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "id_counter",
        sa.Column("entity_type", sa.String(), primary_key=True),
        sa.Column("next_value", sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("id_counter")
