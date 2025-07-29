# app/config.py

from dotenv import load_dotenv
from pydantic import PostgresDsn, EmailStr, SecretStr, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    # Tell Pydantic where to load from
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid"  # 🔒 optional: change to "ignore" if you want leniency
    )

    # Required ENV vars
    database_url: PostgresDsn

    smtp_user: str
    smtp_pass: str
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    # ✅ Add missing env vars here:
    jwt_secret: SecretStr
    vite_api_base_url: HttpUrl

# Instantiate settings
settings = Settings()
