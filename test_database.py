#!/usr/bin/env python3
"""
Test database connection and create tables if needed
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from app.database import engine, Base
    from app.models import User, Task, Notification
    from sqlalchemy import text
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


    def test_connection():
        """Test database connection"""
        try:
            logger.info("🔍 Testing database connection...")

            # Test basic connection
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                logger.info("✅ Database connection successful!")

            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            logger.info(f"📋 Existing tables: {existing_tables}")

            # Create tables if they don't exist
            required_tables = ['users', 'tasks', 'notifications']
            missing_tables = [t for t in required_tables if t not in existing_tables]

            if missing_tables:
                logger.info(f"🔧 Creating missing tables: {missing_tables}")
                Base.metadata.create_all(bind=engine)

                # Check again
                inspector = inspect(engine)
                new_tables = inspector.get_table_names()
                logger.info(f"✅ Tables now available: {new_tables}")
            else:
                logger.info("✅ All required tables exist!")

            return True

        except Exception as e:
            logger.error(f"❌ Database connection failed: {str(e)}")
            logger.error(f"❌ Error type: {type(e).__name__}")

            # Print some debugging info
            db_url = os.getenv('DATABASE_URL', 'Not set')
            logger.error(f"❌ DATABASE_URL: {db_url[:50]}...")

            return False


    if __name__ == "__main__":
        print("🚀 Testing database connection...\n")

        if test_connection():
            print("\n✅ Database is ready for use!")
        else:
            print("\n❌ Database connection failed. Check your DATABASE_URL and network connection.")
            sys.exit(1)

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you have installed all dependencies:")
    print("pip install psycopg2-binary sqlalchemy")
    sys.exit(1)