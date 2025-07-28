import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

from pyexpat.errors import messages
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Task, Notification
from .utils.email_utils import send_email, EmailSchema


sched = AsyncIOScheduler()


def start_scheduler():
    sched.add_job(send_due_reminders, 'interval', minutes=1)
    sched.start()


async def send_due_reminders():
    def db_work():
        db: Session = SessionLocal()
        now = datetime.utcnow()
        soon = now + timedelta(minutes=5)
        tasks = (
            db.query(Task)
            .filter(Task.due_at == soon, Task.due_at >= now, Task.reminded == False)
            .all()
        )
        for task in tasks:
            # build email
            email = EmailSchema(
                email_to=task.user_email,
                subject=f"Reminder: '{task.title}' due at {task.due_at.isoformat()}",
                body=(
                    f"<p>Hi there,</p>"
                    f"<p>Your task <strong>{task.title}</strong> is due on "
                    f"{task.due_at.strftime('%Y-%m-%d %H:%M UTC')}.</p>"
                    f"<p>Description: {task.description or 'No details'}.</p>"
                )
            )

            #create recor of notification
            notif = Notification(
                task_id=task.id,
                message=f"Task '{task.title}' due at {task.due_at.strftime('%Y-%m-%d %H:%M')}.",
            )
            db.add(notif)
            task.notified = True
            db.commit()
            db.refresh(task)
            asyncio.create_task(send_email(email))
        db.close()

    await asyncio.get_event_loop().run_in_executor(None, db_work)




