import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Import all models so they register on Base.metadata before autogenerate diffs it.
import lapp.models  # noqa: F401
from lapp.core.database import Base
from config import config as app_config

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Resolve the DB URL. Precedence: whatever the caller already configured
# (e.g. DatabaseManager.run_migrations() sets sqlalchemy.url from the live
# engine) > -x db_url=... on the alembic CLI > LAPP_ENV-selected app Config.
# Never silently override a URL the caller already provided — this file is
# re-executed by command.stamp()/upgrade() inside the running app process.
if not config.get_main_option("sqlalchemy.url"):
    env_name = os.environ.get("LAPP_ENV", "dev")
    db_url = context.get_x_argument(as_dictionary=True).get("db_url") or app_config[env_name].SQLALCHEMY_DATABASE_URI
    config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_offline() -> None:
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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
