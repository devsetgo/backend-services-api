# -*- coding: utf-8 -*-
"""Application configuration.
Most configuration is set via environment variables.
For local development, use a .env file to set
environment variables.
"""

import secrets
from datetime import datetime
from functools import lru_cache

from pydantic import BaseSettings, EmailStr, validator


class Settings(BaseSettings):
    title: str = "Test API"
    description: str = "Example API to learn from."
    app_version: str = "x.y.z"
    # application configurations
    release_env: str = "prd"
    https_on: bool = True
    prometheus_on: bool = True
    database_type: str = "sqlite"
    db_name: str = "sqlite_db/api.db"
    sqlalchemy_database_uri: str = "sqlite:///sqlite_db/api.db"
    workers: int = 2
    secret_key: str = str(secrets.token_urlsafe(256))
    # loguru settings
    loguru_retention: str = "10 days"
    loguru_rotation: str = "100 MB"
    loguru_logging_level: str = "INFO"
    # default admin
    create_admin: bool = False
    admin_user_name: str = "admin"
    admin_email: EmailStr
    password: str = "rules"
    # Config info
    updated: datetime = datetime.utcnow()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("admin_user_name")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v


@lru_cache()
def get_settings():
    return Settings()


config_settings = get_settings()
