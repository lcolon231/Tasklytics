# rename_columns.py
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()
url = os.getenv("DATABASE_URL")
if not url:
    raise RuntimeError("DATABASE_URL not set")

engine = create_engine(url)

with engine.begin() as conn:
    conn.execute(text("""
    DO $$
    BEGIN
      IF EXISTS (
        SELECT 1 FROM information_schema.columns
         WHERE table_name='tasks' AND column_name='name'
      ) THEN
        ALTER TABLE tasks RENAME COLUMN name TO title;
      END IF;
      IF EXISTS (
        SELECT 1 FROM information_schema.columns
         WHERE table_name='tasks' AND column_name='due_date'
      ) THEN
        ALTER TABLE tasks RENAME COLUMN due_date TO due_at;
      END IF;
    END
    $$;
    """))

print("✅ Columns renamed (if they existed)")
