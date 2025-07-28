from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from .database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    due_at = Column(DateTime, nullable=False, index=True)
    user_email = Column(String, nullable=False, index=True)
    reminded = Column(Boolean, default=False)
    created = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    notifications = relationship("Notification", back_populates="task", cascade="all, delete-orphan")


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    message = Column(String)

    task = relationship("Task", back_populates="notifications")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


if __name__ == "__main__":
    from.database import engine
    Base.metadata.create_all(bind=engine)