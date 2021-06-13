# -*- coding: utf-8 -*-
# """
# Database configuration and schema
# """
# from databases import Database
# from loguru import logger
# from sqlalchemy import (
#     JSON,
#     Boolean,
#     Column,
#     Integer,
#     String,
#     DateTime,
#     MetaData,
#     String,
#     Table,
#     create_engine,
# )
# from sqlalchemy.pool import QueuePool

# from settings import config_settings

# engine = create_engine(
#     config_settings.sqlalchemy_database_uri,
#     poolclass=QueuePool,
#     max_overflow=40,
#     pool_size=200,
# )

# metadata = MetaData()
# database = Database(config_settings.sqlalchemy_database_uri)


# def create_db():
#     metadata.create_all(engine)
#     logger.info("Creating tables")


# async def connect_db():
#     await database.connect()
#     logger.info(f"connecting to database {config_settings.sqlalchemy_database_uri}")


# async def disconnect_db():
#     await database.disconnect()
#     logger.info("disconnecting from database")


# from sqlalchemy.orm import relationship
# from sqlalchemy.sql.schema import ForeignKey

# users = Table(
#     "users",
#     metadata,
#     Column("id", String(length=100), primary_key=True),
#     Column("user_name", String(length=50), unique=True, nullable=False),
#     Column("email", String(length=200), unique=True, nullable=False),
#     Column("password", String(length=50)),
#     Column("notes", String(length=2000)),
#     Column("date_created", DateTime()),
#     Column("date_updated", DateTime()),
#     Column("last_login", DateTime()),
#     Column("is_active", Boolean(), default=True),
#     Column("is_admin", Boolean(), default=True),
#     Column("is_approved", Boolean(), default=False),
#     # relationship("roles", back_populates="users"),
# )

# roles = Table(
#     "roles",
#     metadata,
#     Column("id", String(length=100), primary_key=True),
#     Column("is_active", Boolean(), default=False),
#     Column("name", String(length=50), unique=True, nullable=False),
#     Column("description", String(length=200), unique=True, nullable=False),
#     Column("id_user", String(), ForeignKey("users.id")),
#     Column("user_id", String(), ForeignKey("users.id"), nullable=False),
# )


# email_service = Table(
#     "email_service",
#     metadata,
#     Column("id", String(length=100), primary_key=True),
#     Column("sent", Boolean(), default=False),
#     Column("email_content", JSON()),
#     Column("user_id", String(length=100)),
#     Column("app_id", String(length=100)),
# )

# applications = Table(
#     "applications",
#     metadata,
#     Column("id", String(length=100), primary_key=True),
#     Column("name", String(length=100), unique=True, nullable=False),
#     Column("description", String(length=500)),
#     Column("date_created", DateTime()),
#     Column("date_update", DateTime()),
#     Column("user_id", String(length=100)),
# )

# app_log = Table(
#     "app_log",
#     metadata,
#     Column("id", String(length=100), primary_key=True),
#     Column("app_id", String(length=100)),
#     Column("level", String(length=100)),
#     Column("data", JSON()),
#     Column("date_created", DateTime()),
# )
