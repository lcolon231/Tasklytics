# scripts/fix_null_created.py

from app.database import SessionLocal
from sqlalchemy import text


def fix_null_created():
    db = SessionLocal()
    try:
        db.execute(text("UPDATE tasks SET created = NOW() WHERE created IS NULL"))
        db.commit()
        print("✅ Null 'created' fields updated successfully.")
    except Exception as e:
        print("❌ Error:", e)
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    fix_null_created()
