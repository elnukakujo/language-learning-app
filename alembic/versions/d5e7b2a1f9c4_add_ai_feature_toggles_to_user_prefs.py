"""add ai_feedback_enabled, ai_text_gen_enabled, ai_tts_enabled to user_preferences

Revision ID: d5e7b2a1f9c4
Revises: c4f2a8e1d7b3
Create Date: 2026-07-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd5e7b2a1f9c4'
down_revision: Union[str, Sequence[str], None] = 'c4f2a8e1d7b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user_preferences', sa.Column('ai_feedback_enabled', sa.Boolean(), nullable=False, server_default=sa.true()))
    op.add_column('user_preferences', sa.Column('ai_text_gen_enabled', sa.Boolean(), nullable=False, server_default=sa.true()))
    op.add_column('user_preferences', sa.Column('ai_tts_enabled', sa.Boolean(), nullable=False, server_default=sa.true()))


def downgrade() -> None:
    op.drop_column('user_preferences', 'ai_tts_enabled')
    op.drop_column('user_preferences', 'ai_text_gen_enabled')
    op.drop_column('user_preferences', 'ai_feedback_enabled')
