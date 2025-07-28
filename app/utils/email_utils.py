import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from app.config import settings
from dotenv import load_dotenv
from fastapi import BackgroundTasks

load_dotenv()

# Email config from .env via app.config.settings
mail_conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_USERNAME"),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS", "true").lower() == "true",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS", "false").lower() == "true",
    USE_CREDENTIALS=True,

)


# General email schema
class EmailSchema(BaseModel):
    email_to: EmailStr
    subject: str
    message: str


# Generic async email sender
async def send_email(email: EmailSchema):
    message = MessageSchema(
        subject=email.subject,
        recipients=[email.email_to],
        body=email.message,
        subtype="html"
    )
    fm = FastMail(mail_conf)
    await fm.send_message(message)


# Background-compatible password reset sender
def send_password_reset_email(background_tasks: BackgroundTasks, to_email: str, reset_link: str):
    email = EmailSchema(
        email_to=to_email,
        subject="Password Reset Request",
        message=f"""
            <h2>Password Reset</h2>
            <p>You requested a password reset. Click the link below to reset your password:</p>
            <a href="{reset_link}">{reset_link}</a>
            <p>This link will expire in 15 minutes.</p>
            <p>If you didn't request this, you can safely ignore this email.</p>
        """
    )
    background_tasks.add_task(send_email, email)
