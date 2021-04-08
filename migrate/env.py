# coding: utf8

"""
export CONFIG=path...
alembic revision -m "commit message" --autogenerate --head head
alembic upgrade head
"""

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.split(dir_path)[0])

from app.configure import ConfigReader
from app.database.models import db


config = context.config
fileConfig(config.config_file_name)

target_metadata = db
reader = ConfigReader().setup()

db_cfg = reader.database()
url = (f'postgresql://'
       f'{db_cfg.APP_DB_LOGIN}:'
       f'{db_cfg.APP_DB_PASSWORD}@'
       f'{db_cfg.APP_DB_HOST}/'
       f'{db_cfg.APP_DB_NAME}')


def run_migrations_offline():
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=False,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    config_dict = config.get_section(config.config_ini_section)
    config_dict['sqlalchemy.url'] = url

    connectable = engine_from_config(
        config_dict,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
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
