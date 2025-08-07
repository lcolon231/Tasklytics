from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Notification, User
from app.schemas import NotificationOut, NotificationCreate
from app.auth.dependencies import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[NotificationOut])
def list_user_notifications(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get notifications for the current user's tasks"""
    # Join with tasks to filter by user
    notifications = (
        db.query(Notification)
        .join(Notification.task)
        .filter(Notification.task.has(user_email=current_user.email))
        .order_by(Notification.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return notifications


@router.get("/{notification_id}", response_model=NotificationOut)
def get_notification(
        notification_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get a specific notification if it belongs to the current user"""
    notification = (
        db.query(Notification)
        .join(Notification.task)
        .filter(
            Notification.id == notification_id,
            Notification.task.has(user_email=current_user.email)
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    return notification


@router.post("/", response_model=NotificationOut, status_code=status.HTTP_201_CREATED)
def create_notification(
        notification: NotificationCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Create a new notification (admin/system use)"""
    # Verify the task belongs to the current user
    from app.models import Task
    task = db.query(Task).filter(
        Task.id == notification.task_id,
        Task.user_email == current_user.email
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db_notification = Notification(
        task_id=notification.task_id,
        message=notification.message
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
        notification_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Delete a notification if it belongs to the current user"""
    notification = (
        db.query(Notification)
        .join(Notification.task)
        .filter(
            Notification.id == notification_id,
            Notification.task.has(user_email=current_user.email)
        )
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    db.delete(notification)
    db.commit()
    return None


@router.get("/unread/count")
def get_unread_count(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get count of unread notifications for the current user"""
    # This would require adding a 'read' field to the Notification model
    # For now, just return total count
    count = (
        db.query(Notification)
        .join(Notification.task)
        .filter(Notification.task.has(user_email=current_user.email))
        .count()
    )
    return {"unread_count": count}