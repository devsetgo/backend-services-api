# -*- coding: utf-8 -*-
"""Application configuration.
Most configuration is set via environment variables.
For local development, use a .env file to set
environment variables.
"""

import secrets
from datetime import datetime
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings


class Settings(BaseSettings):
    title: str = "Test API"
    description: str = "Example API to learn from."
    app_version: str = "1.0.0"
    owner: str = "Mike Ryan"
    website: AnyUrl = "https://devsetgo.com"
    license_type: str = "MIT"
    license_link: AnyUrl = "https://github.com/devsetgo/test-api/blob/master/LICENSE"
    # application configurations
    host_domain: AnyUrl = "https://test-api.devsetgo.com"
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
    # Config info
    updated: datetime = datetime.utcnow()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


config_settings = get_settings()
