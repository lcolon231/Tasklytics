import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal
from app.models import Notification

def show_notifications():
    db = SessionLocal()
    try:
        notifications = db.query(Notification).all()
        print(f"{len(notifications)} notifications found: ")
        for n in notifications:
            print(f"{n.id}, TASK ID: {n.task_id}, Created at: {n.created_at}, Message: {n.message}")
    finally:
        db.close()

if __name__ == "__main__":
    show_notifications()