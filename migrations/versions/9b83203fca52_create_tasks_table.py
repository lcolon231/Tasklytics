"""create tasks table

Revision ID: 9b83203fca52
Revises: fd3087ec1151
Create Date: 2025-07-18 19:58:41.223397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b83203fca52'
down_revision: Union[str, Sequence[str], None] = 'fd3087ec1151'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('tilte', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=False),
        sa.Column('due_at', sa.DateTime(), nullable=False),
        sa.Column("user_email", sa.String(length=255), nullable=False),
        sa.Column('reminded', sa.Boolean(), nullable=False),
    )


def downgrade():
    op.drop_table('tasks')
