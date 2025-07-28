import os
from logging.config import fileConfig
import app.models
from sqlalchemy import engine_from_config, pool
from alembic import context

# — Load your .env so DATABASE_URL is available
from dotenv import load_dotenv
load_dotenv()

# this is the Alembic Config object, which provides
# access to values from alembic.ini.
config = context.config

# — Override the sqlalchemy.url setting with your env var
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL is not set in environment or .env")
config.set_main_option("sqlalchemy.url", db_url)

# Interpret the config file for Python logging.
# This sets up loggers based on [loggers], [handlers], etc., in alembic.ini.
if config.config_file_name:
    fileConfig(config.config_file_name)

# — Import your app’s Base metadata for 'autogenerate' support
#    Adjust the import path if your structure differs.
from app.database import Base

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (no DBAPI needed)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (connects to the database)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


# Choose offline vs. online based on context
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
