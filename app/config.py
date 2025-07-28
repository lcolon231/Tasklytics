# app/config.py

from dotenv import load_dotenv
from pydantic import PostgresDsn, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Database
    database_url: PostgresDsn

    # Legacy/unnecessary (can be removed if unused elsewhere)
    smtp_user: str
    smtp_pass: str
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587

    # Email for FastAPI-Mail
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    # ✅ Add these two for ConnectionConfig
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False


# Instantiate
settings = Settings()

