from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.models import User
from app.schemas import UserOut, UserRead
from app.auth.dependencies import get_current_active_user

router = APIRouter()


@router.get("/me", response_model=UserOut)
def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user's profile"""
    return current_user


@router.put("/me", response_model=UserOut)
def update_current_user_profile(
        updates: dict,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    """Update current user's profile (non-sensitive fields only)"""
    # Only allow updating certain fields
    allowed_fields = {'first_name', 'last_name', 'age'}

    for field, value in updates.items():
        if field in allowed_fields:
            setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/{user_id}", response_model=UserRead)
def get_user_profile(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get another user's public profile (limited info)"""
    # Users can only see their own profile or limited info of others
    if user_id == current_user.id:
        return current_user

    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Return limited information for other users
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email  # You might want to hide this for privacy
    }


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user_account(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    """Deactivate current user's account (soft delete)"""
    # Soft delete - set is_active to False instead of actually deleting
    current_user.is_active = False
    db.commit()
    return None


# Admin endpoints (would need admin role checking)
@router.get("/", response_model=List[UserRead])
def list_all_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """List all users (admin only - implement role checking)"""
    # TODO: Add admin role checking
    # For now, any authenticated user can see this (not recommended for production)
    users = db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    return users