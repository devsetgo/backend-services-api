# -*- coding: utf-8 -*-

import databases
from loguru import logger
from sqlalchemy import Boolean
from sqlalchemy import Column, JSON
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

from settings import SQLALCHEMY_DATABASE_URI

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, poolclass=QueuePool, max_overflow=10, pool_size=100
)
metadata = MetaData()
database = databases.Database(SQLALCHEMY_DATABASE_URI)


def create_db():
    metadata.create_all(engine)
    logger.info(f"Creating tables")


async def connect_db():
    await database.connect()
    logger.info(f"connecting to database")


async def disconnect_db():
    await database.disconnect()
    logger.info(f"disconnecting from database")


users = Table(
    "users",
    metadata,
    # Column('Id', Integer, primary_key=True),
    Column("user_id", String(length=100), primary_key=True),
    Column("user_name", String(length=50), unique=True, nullable=False),
    Column("first_name", String(length=150)),
    Column("last_name", String(length=150)),
    Column("title", String(length=200)),
    Column("company", String(length=200)),
    Column("address", String(length=300)),
    Column("city", String(length=200)),
    Column("country", String(length=200)),
    Column("postal", String(length=50)),
    Column("phone", String(length=50)),
    Column("email", String(length=200), unique=True, nullable=False),
    Column("website", String(length=150)),
    Column("password", String(length=50)),
    Column("description", String(length=2000)),
    Column("date_create", DateTime()),
    Column("date_updated", DateTime()),
    Column("is_active", Boolean(), default=True),
    Column("is_superuser", Boolean(), default=True),
)


app_config = Table(
    "app_config",
    metadata,
    Column("config_id", String, primary_key=True),
    Column("config_name", String(length=50), unique=True, nullable=False),
    Column("config_version", String(length=20)),
    Column("configuration_data", JSON),
    Column("description", String(length=2000)),
    Column("date_create", DateTime()),
    Column("date_updated", DateTime()),
    Column("is_active", Boolean(), default=True),
)
# Foreign key Column('userId', None, ForeignKey('users.userId')),
