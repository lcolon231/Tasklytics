# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool


# 1️⃣ Bring in your FastAPI app
from app.main import app

# 2️⃣ Bring in Base (to create tables) and your DB-dep
from app.database import Base
from app.dependencies import get_db

# 3️⃣ Import your models so Base.metadata knows about Task
from app import models

# 4️⃣ Set up an in-memory SQLite for tests
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# 5️⃣ Create all tables in that test DB
Base.metadata.create_all(bind=engine)

# 6️⃣ Override the get_db dependency to use the test session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 7️⃣ Provide a TestClient fixture
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
