"""replace ai_text_gen_enabled with granular text-gen toggles, add per-user AI API overrides

Revision ID: f2a917c6b8d1
Revises: d5e7b2a1f9c4
Create Date: 2026-07-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f2a917c6b8d1'
down_revision: Union[str, Sequence[str], None] = 'd5e7b2a1f9c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user_preferences', sa.Column('ai_learnable_sentence_enabled', sa.Boolean(), nullable=False, server_default=sa.true()))
    op.add_column('user_preferences', sa.Column('ai_example_sentence_enabled', sa.Boolean(), nullable=False, server_default=sa.true()))
    op.add_column('user_preferences', sa.Column('ai_example_word_enabled', sa.Boolean(), nullable=False, server_default=sa.true()))
    op.add_column('user_preferences', sa.Column('ai_gen_api_base_url', sa.String(), nullable=True))
    op.add_column('user_preferences', sa.Column('ai_gen_api_key', sa.String(), nullable=True))
    op.add_column('user_preferences', sa.Column('ai_gen_model', sa.String(), nullable=True))
    op.add_column('user_preferences', sa.Column('ai_tts_api_base_url', sa.String(), nullable=True))
    op.add_column('user_preferences', sa.Column('ai_tts_api_key', sa.String(), nullable=True))
    op.add_column('user_preferences', sa.Column('ai_tts_model', sa.String(), nullable=True))
    op.drop_column('user_preferences', 'ai_text_gen_enabled')


def downgrade() -> None:
    op.add_column('user_preferences', sa.Column('ai_text_gen_enabled', sa.Boolean(), nullable=False, server_default=sa.true()))
    op.drop_column('user_preferences', 'ai_tts_model')
    op.drop_column('user_preferences', 'ai_tts_api_key')
    op.drop_column('user_preferences', 'ai_tts_api_base_url')
    op.drop_column('user_preferences', 'ai_gen_model')
    op.drop_column('user_preferences', 'ai_gen_api_key')
    op.drop_column('user_preferences', 'ai_gen_api_base_url')
    op.drop_column('user_preferences', 'ai_example_word_enabled')
    op.drop_column('user_preferences', 'ai_example_sentence_enabled')
    op.drop_column('user_preferences', 'ai_learnable_sentence_enabled')
