from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.dependencies import get_db
from app.models import Task, User
from app.schemas import TaskCreate, TaskOut, TaskUpdate
from app.auth.dependencies import get_current_active_user

router = APIRouter()


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
        task: TaskCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Create a new task"""
    db_task = Task(
        title=task.title,
        description=task.description,
        due_at=task.due_at,
        user_email=current_user.email
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/", response_model=List[TaskOut])
def get_tasks(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get tasks for the current user"""
    tasks = db.query(Task).filter(
        Task.user_email == current_user.email
    ).offset(skip).limit(limit).all()
    return tasks


# FIXED: Move this endpoint BEFORE the /{task_id} endpoint to avoid conflicts
@router.get("/upcoming", response_model=List[TaskOut])
def get_upcoming_tasks(
        hours: int = 24,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get tasks due in the next X hours"""
    now = datetime.utcnow()
    future = now + timedelta(hours=hours)

    tasks = db.query(Task).filter(
        Task.user_email == current_user.email,
        Task.due_at >= now,
        Task.due_at <= future
    ).order_by(Task.due_at).all()

    return tasks


@router.get("/overdue", response_model=List[TaskOut])
def get_overdue_tasks(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get overdue tasks"""
    now = datetime.utcnow()

    tasks = db.query(Task).filter(
        Task.user_email == current_user.email,
        Task.due_at < now
    ).order_by(Task.due_at).all()

    return tasks


@router.get("/stats")
def get_task_stats(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get task statistics for the current user"""
    now = datetime.utcnow()

    total_tasks = db.query(Task).filter(
        Task.user_email == current_user.email
    ).count()

    overdue_tasks = db.query(Task).filter(
        Task.user_email == current_user.email,
        Task.due_at < now
    ).count()

    upcoming_tasks = db.query(Task).filter(
        Task.user_email == current_user.email,
        Task.due_at >= now,
        Task.due_at <= now + timedelta(hours=24)
    ).count()

    return {
        "total_tasks": total_tasks,
        "overdue_tasks": overdue_tasks,
        "upcoming_tasks": upcoming_tasks
    }


@router.get("/{task_id}", response_model=TaskOut)
def get_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get a specific task"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_email == current_user.email
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
        task_id: int,
        task_update: TaskUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Update a task"""
    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_email == current_user.email
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update fields
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db_task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Delete a task"""
    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_email == current_user.email
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(db_task)
    db.commit()
    return None