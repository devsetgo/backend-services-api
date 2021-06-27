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
    # database configuration
    db_name: str = "api.db"
    db_dialect: str = "sqlite"
    db_url: str = "sqlite_db"
    db_user: str = None
    db_pwd: str = None
    # database_uri: str = "sqlite:///sqlite_db/api.db"
    workers: int = 2
    secret_key: str = str(secrets.token_urlsafe(256))
    # loguru settings
    loguru_retention: str = "10 days"
    loguru_rotation: str = "100 MB"
    loguru_logging_level: str = "INFO"
    # default admin
    create_admin: bool = False
    admin_user_name: str = None
    admin_email: EmailStr = None
    admin_password: str = None
    # Config info
    updated: datetime = datetime.utcnow()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        allow_mutation = True

    @validator("admin_user_name")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v


@lru_cache()
def get_settings():
    return Settings()


config_settings = get_settings()
