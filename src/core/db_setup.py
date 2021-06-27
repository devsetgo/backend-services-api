# -*- coding: utf-8 -*-
"""
Database configuration and schema
"""
from databases import Database
from loguru import logger
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    MetaData,
    String,
    Table,
    create_engine,
)
from sqlalchemy.pool import QueuePool
from pathlib import Path
from settings import config_settings

if config_settings.db_dialect.lower() == "postgresql":
    database_uri: str = f"{config_settings.db_dialect}://{config_settings.db_user}:{config_settings.db_pwd}@{config_settings.db_url}/{config_settings.db_name}"

elif config_settings.db_dialect.lower() == "sqlite":
    cwd = Path.cwd()
    p = cwd.parent

    if config_settings.release_env != "test":
        db_path = p.joinpath("sqlite_db").joinpath(f"{config_settings.db_name}.db")
    else:
        # set path for test db
        db_path = p.joinpath("sqlite_db").joinpath("test.db")

    database_uri: str = f"{config_settings.db_dialect}:///{db_path}"

logger.debug(f"DB URI: {database_uri}")

engine = create_engine(
    database_uri,
    poolclass=QueuePool,
    max_overflow=40,
    pool_size=200,
)
database = Database(database_uri)

metadata = MetaData()


def create_db():
    metadata.create_all(engine)
    logger.info("Creating tables")


async def connect_db():
    await database.connect()
    logger.info(f"connecting to database {config_settings.sqlalchemy_database_uri}")


async def disconnect_db():
    await database.disconnect()
    logger.info("disconnecting from database")


from sqlalchemy.sql.schema import ForeignKey

users = Table(
    "users",
    metadata,
    Column("id", String(length=100), primary_key=True),
    Column("user_name", String(length=50), unique=True, nullable=False),
    Column("email", String(length=200), unique=True, nullable=False),
    Column("password", String(length=50)),
    Column("notes", String(length=2000)),
    Column("date_created", DateTime()),
    Column("date_updated", DateTime()),
    Column("last_login", DateTime()),
    Column("is_active", Boolean(), default=True),
    Column("is_admin", Boolean(), default=True),
    Column("is_approved", Boolean(), default=False),
    # relationship("roles", back_populates="users"),
)

roles = Table(
    "roles",
    metadata,
    Column("id", String(length=100), primary_key=True),
    Column("is_active", Boolean(), default=False),
    Column("name", String(length=50), unique=True, nullable=False),
    Column("description", String(length=200), unique=True, nullable=False),
    Column("id_user", String(), ForeignKey("users.id")),
    Column("user_id", String(), ForeignKey("users.id"), nullable=False),
)

applications = Table(
    "applications",
    metadata,
    Column("id", String(length=100), primary_key=True),
    Column("name", String(length=50), unique=True, nullable=False),
    Column("description", String(length=20)),
    Column("user_id", String(length=50), nullable=False),
    Column("is_active", Boolean()),
    Column("date_created", DateTime()),
    Column("date_updated", DateTime()),
)

audit_log = Table(
    "audit_log",
    metadata,
    Column("id", String(length=100), primary_key=True),
    Column("app_id", String(length=50)),
    Column("record_type", String(length=20)),
    Column("record_str", String(length=500)),
    Column("record_json", JSON()),
    Column("date_created", DateTime()),
)

logging_info = Table(
    "logging_info",
    metadata,
    Column("id", String(length=100), primary_key=True),
    Column("app_id", String(length=50), nullable=False),
    Column("reference_id", String(length=50), nullable=False),
    Column("record_str", String(length=500)),
    Column("record_json", JSON()),
    Column("record_date", DateTime()),
    Column("date_created", DateTime()),
)
email_service = Table(
    "email_service",
    metadata,
    Column("id", String(length=100), primary_key=True),
    Column("sent", Boolean(), default=False),
    Column("email_content", JSON()),
    Column("user_id", String(length=100)),
    Column("app_id", String(length=100)),
)
