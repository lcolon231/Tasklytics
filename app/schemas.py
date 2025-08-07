from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: str
    due_at: datetime
    user_email: str


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_at: datetime
    user_email: EmailStr


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_at: Optional[datetime] = None
    user_email: Optional[EmailStr] = None
    reminded: Optional[bool] = None


class TaskRead(TaskBase):
    id: int
    reminded: bool


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    due_at: datetime
    user_email: EmailStr
    reminded: bool
    created: datetime

    model_config = ConfigDict(from_attributes=True)


class NotificationCreate(BaseModel):
    task_id: int
    message: str


class NotificationOut(BaseModel):
    id: int
    task_id: int
    message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    age: int


class UserRead(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str