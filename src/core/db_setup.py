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
    Date,
    DateTime,
    MetaData,
    String,
    Table,
    create_engine,
)
from sqlalchemy.pool import QueuePool

from settings import config_settings

engine = create_engine(
    config_settings.sqlalchemy_database_uri,
    poolclass=QueuePool,
    max_overflow=40,
    pool_size=200,
)

metadata = MetaData()
database = Database(config_settings.sqlalchemy_database_uri)


def create_db():
    metadata.create_all(engine)
    logger.info("Creating tables")


async def connect_db():
    await database.connect()
    logger.info(f"connecting to database {config_settings.sqlalchemy_database_uri}")


async def disconnect_db():
    await database.disconnect()
    logger.info("disconnecting from database")


logging = Table(
    "logging",
    metadata,
    Column("id", String, primary_key=True),
    Column("app_id", String(length=100)),
    Column("description", String()),
    Column("date_create", DateTime()),
)

users = Table(
    "users",
    metadata,
    Column("id", String, primary_key=True),
    Column("name", String(length=50), unique=True, nullable=False),
    Column("email", String(length=200), unique=True, nullable=False),
    Column("password", String(length=50)),
    Column("admin", Boolean(), default=False),
    Column("is_active", Boolean(), default=False),
    Column("date_create", DateTime()),
    Column("date_update", DateTime()),
)
application = Table(
    "application",
    metadata,
    Column("id", String, primary_key=True),
    Column("name", String(length=50), unique=True, nullable=False),
    Column("user", String(length=50), unique=True, nullable=False),
    Column("is_active", Boolean(), default=False),
    Column("date_create", DateTime()),
    Column("date_update", DateTime()),
)