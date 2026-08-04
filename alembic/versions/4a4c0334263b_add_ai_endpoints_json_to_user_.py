"""add_ai_endpoints_json_to_user_preferences

Revision ID: 4a4c0334263b
Revises: f2a917c6b8d1
Create Date: 2026-08-02 20:36:38.876439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a4c0334263b'
down_revision: Union[str, Sequence[str], None] = 'f2a917c6b8d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user_preferences', sa.Column('ai_endpoints', sa.JSON(), nullable=True, server_default='[]'))


def downgrade() -> None:
    op.drop_column('user_preferences', 'ai_endpoints')
