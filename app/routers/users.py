# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.models import User
from app.schemas import UserCreate, UserRead
from passlib.context import CryptContext

router = APIRouter()

# Password‐hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserRead, tags=["users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    # Check for existing email
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the plain‐text password
    hashed_password = pwd_context.hash(user.password)

    # Create and persist
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UserRead], tags=["users"])
def list_users(db: Session = Depends(get_db)):
    """
    List all users.
    """
    return db.query(User).all()

@router.get("/{user_id}", response_model=UserRead, tags=["users"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single user by ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
