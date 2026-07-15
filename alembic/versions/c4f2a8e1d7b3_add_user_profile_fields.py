"""add display_name, email, password_hash to user

Revision ID: c4f2a8e1d7b3
Revises: b1e4a6f930cd
Create Date: 2026-07-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c4f2a8e1d7b3'
down_revision: Union[str, Sequence[str], None] = 'b1e4a6f930cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('display_name', sa.String(), nullable=True))
    op.add_column('user', sa.Column('email', sa.String(), nullable=True))
    op.create_unique_constraint('uq_user_email', 'user', ['email'])
    op.add_column('user', sa.Column('password_hash', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('user', 'password_hash')
    op.drop_constraint('uq_user_email', 'user', type_='unique')
    op.drop_column('user', 'email')
    op.drop_column('user', 'display_name')
