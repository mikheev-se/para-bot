from logging.config import fileConfig

from sqlalchemy import create_engine, engine_from_config
from sqlalchemy import pool

from alembic import context
from core.settings import settings

from src.entities import base, name, surname, subject

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = base.Base.metadata


def run_migrations_offline() -> None:
    url = settings.db_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(settings.db_url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
