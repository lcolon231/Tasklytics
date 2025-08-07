import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import BaseModel, EmailStr
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from app.config import settings

logger = logging.getLogger(__name__)

# Thread pool for sending emails
email_executor = ThreadPoolExecutor(max_workers=5)


class EmailSchema(BaseModel):
    email_to: EmailStr
    subject: str
    body: str


def _send_email_sync(message: MIMEMultipart) -> bool:
    """Synchronous email sending function for thread executor"""
    try:
        with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
            if settings.mail_starttls:
                server.starttls()

            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            server.send_message(message)

        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False


async def send_email(email: EmailSchema) -> bool:
    """Send email using SMTP configuration from settings (async)"""
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = email.subject
        message["From"] = settings.MAIL_FROM
        message["To"] = email.email_to

        # Create HTML part
        html_part = MIMEText(email.body, "html")
        message.attach(html_part)

        # Send email in thread executor to avoid blocking
        loop = asyncio.get_event_loop()
        success = await loop.run_in_executor(email_executor, _send_email_sync, message)

        if success:
            logger.info(f"Email sent successfully to {email.email_to}")
        else:
            logger.error(f"Failed to send email to {email.email_to}")

        return success

    except Exception as e:
        logger.error(f"Failed to send email to {email.email_to}: {str(e)}")
        return False


# Keep the synchronous version for background tasks compatibility
def send_password_reset_email(email_to: str, reset_token: str, user_name: str) -> bool:
    """Send password reset email with reset link (synchronous for BackgroundTasks)"""
    try:
        # Build frontend URL for password reset
        frontend_url = str(settings.vite_api_base_url).replace('/api', '')
        reset_url = f"{frontend_url}/reset-password?token={reset_token}"

        subject = "Password Reset Request - Task Tracker"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center;">
                    <h1 style="margin: 0; font-size: 28px;">🔐 Password Reset Request</h1>
                </div>

                <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                    <p style="font-size: 16px; margin-bottom: 20px;">Hi <strong>{user_name}</strong>,</p>

                    <p style="margin-bottom: 20px;">You requested a password reset for your Task Tracker account. No worries - it happens to the best of us!</p>

                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_url}" 
                           style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                  color: white; 
                                  padding: 15px 30px; 
                                  text-decoration: none; 
                                  border-radius: 25px; 
                                  font-weight: bold; 
                                  font-size: 16px;
                                  display: inline-block;
                                  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);">
                            Reset My Password
                        </a>
                    </div>

                    <p style="margin-bottom: 15px; font-size: 14px; color: #666;">If the button doesn't work, copy and paste this link into your browser:</p>
                    <p style="background: #e9ecef; padding: 10px; border-radius: 5px; font-family: monospace; word-break: break-all; font-size: 12px;">
                        <a href="{reset_url}" style="color: #667eea;">{reset_url}</a>
                    </p>

                    <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 15px; margin: 20px 0;">
                        <p style="margin: 0; font-size: 14px; color: #856404;">
                            ⚠️ <strong>Important:</strong> This link will expire in 1 hour for security reasons.
                        </p>
                    </div>

                    <p style="font-size: 14px; color: #666; margin-top: 30px;">
                        If you didn't request this password reset, please ignore this email. Your account remains secure.
                    </p>

                    <div style="border-top: 1px solid #dee2e6; margin-top: 30px; padding-top: 20px; text-align: center;">
                        <p style="margin: 0; color: #666; font-size: 14px;">
                            Best regards,<br>
                            <strong>The Task Tracker Team</strong> 🚀
                        </p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.MAIL_FROM
        message["To"] = email_to

        # Create HTML part
        html_part = MIMEText(body, "html")
        message.attach(html_part)

        # Send email synchronously
        with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
            if settings.mail_starttls:
                server.starttls()

            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            server.send_message(message)

        logger.info(f"Password reset email sent successfully to {email_to}")
        return True

    except Exception as e:
        logger.error(f"Failed to send password reset email to {email_to}: {str(e)}")
        return False


async def send_task_reminder_email(email_to: str, task_title: str, task_description: str, due_at: str,
                                   user_name: str) -> bool:
    """Send task reminder email"""
    try:
        subject = f"⏰ Reminder: '{task_title}' is due soon!"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #ff7675 0%, #fd79a8 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center;">
                    <h1 style="margin: 0; font-size: 28px;">⏰ Task Reminder</h1>
                </div>

                <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                    <p style="font-size: 16px; margin-bottom: 20px;">Hi <strong>{user_name}</strong>,</p>

                    <p style="margin-bottom: 20px;">This is a friendly reminder that your task is due soon!</p>

                    <div style="background: white; border-left: 4px solid #ff7675; padding: 20px; margin: 20px 0; border-radius: 0 5px 5px 0;">
                        <h3 style="margin: 0 0 10px 0; color: #ff7675;">📋 {task_title}</h3>
                        <p style="margin: 0 0 10px 0; color: #666;"><strong>Due:</strong> {due_at}</p>
                        <p style="margin: 0; color: #666;"><strong>Description:</strong> {task_description or 'No description provided'}</p>
                    </div>

                    <p style="font-size: 14px; color: #666; margin-top: 30px;">
                        Don't forget to mark it as complete once you're done! 💪
                    </p>

                    <div style="border-top: 1px solid #dee2e6; margin-top: 30px; padding-top: 20px; text-align: center;">
                        <p style="margin: 0; color: #666; font-size: 14px;">
                            Stay productive,<br>
                            <strong>Task Tracker</strong> 🎯
                        </p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        # Create and send email
        email_schema = EmailSchema(
            email_to=email_to,
            subject=subject,
            body=body
        )

        success = await send_email(email_schema)

        if success:
            logger.info(f"Task reminder email sent successfully to {email_to}")

        return success

    except Exception as e:
        logger.error(f"Failed to send task reminder email to {email_to}: {str(e)}")
        return False