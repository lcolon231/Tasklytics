"""rename name & due_date columns

Revision ID: aa9af6064728
Revises: 9b83203fca52
Create Date: 2025-07-18 20:43:51.066199

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa9af6064728'
down_revision: Union[str, Sequence[str], None] = '9b83203fca52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # only rename if the old column is still around
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name   = 'tasks'
                  AND column_name  = 'name'
            ) THEN
                ALTER TABLE tasks RENAME COLUMN name TO title;
            END IF;
            IF EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name   = 'tasks'
                  AND column_name  = 'due_date'
            ) THEN
                ALTER TABLE tasks RENAME COLUMN due_date TO due_at;
            END IF;
        END
        $$;
        """
    )


def downgrade():
    op.execute("ALTER TABLE tasks RENAME COLUMN title TO name;")
    op.execute("ALTER TABLE tasks RENAME COLUMN due_at TO due_date;")
