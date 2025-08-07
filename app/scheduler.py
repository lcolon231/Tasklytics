import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import logging

from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Task, Notification
from .utils.email_utils import send_task_reminder_email

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sched = AsyncIOScheduler()


def start_scheduler():
    sched.add_job(send_due_reminders, 'interval', minutes=1)
    sched.start()
    logger.info("Scheduler started - checking for due reminders every minute")


async def send_due_reminders():
    def db_work():
        db: Session = SessionLocal()
        try:
            now = datetime.utcnow()
            # Check for tasks due in the next 5 minutes
            soon = now + timedelta(minutes=5)

            tasks = (
                db.query(Task)
                .filter(
                    Task.due_at <= soon,
                    Task.due_at >= now,
                    Task.reminded == False
                )
                .all()
            )

            logger.info(f"Found {len(tasks)} tasks requiring reminders")

            for task in tasks:
                try:
                    # Create record of notification first
                    notif = Notification(
                        task_id=task.id,
                        message=f"Task '{task.title}' due at {task.due_at.strftime('%Y-%m-%d %H:%M')}.",
                    )
                    db.add(notif)

                    # Mark task as reminded
                    task.reminded = True
                    db.commit()
                    db.refresh(task)

                    # Schedule email sending (async)
                    asyncio.create_task(send_task_reminder_email(
                        email_to=task.user_email,
                        task_title=task.title,
                        task_description=task.description,
                        due_at=task.due_at.strftime('%Y-%m-%d %H:%M UTC'),
                        user_name="User"  # You might want to get actual user name from User table
                    ))

                    logger.info(f"Reminder sent for task: {task.title}")

                except Exception as e:
                    logger.error(f"Error processing task {task.id}: {str(e)}")
                    db.rollback()

        except Exception as e:
            logger.error(f"Error in send_due_reminders: {str(e)}")
        finally:
            db.close()

    await asyncio.get_event_loop().run_in_executor(None, db_work)