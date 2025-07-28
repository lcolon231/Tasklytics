# test_email.py
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load vars from .env
load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_ADDR = os.getenv("MAIL_FROM_ADDRESS", SMTP_USER)
TO_ADDR = "luis.acolon03@gmail.com"   # ← change this

# Build the message
msg = MIMEText("Hey there! This is a test email from Tasklytics. 🚀")
msg["Subject"] = "🚨 SMTP Test Email"
msg["From"] = FROM_ADDR
msg["To"] = TO_ADDR

try:
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()                     # upgrade to TLS
        server.login(SMTP_USER, SMTP_PASS)    # authenticate
        server.send_message(msg)
    print(f"✅ Test email sent to {TO_ADDR}!")
except Exception as e:
    print("❌ Failed to send test email:", e)
