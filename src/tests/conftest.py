# -*- coding: utf-8 -*-
import pytest
import os
from src.settings import Settings, config_settings

config_settings.app_version = "1.2.3"
config_settings.sqlalchemy_database_uri = "sqlite:///sqlite_db/test.db"


@pytest.fixture
def settings_override():
    Settings(_env_file=".env_test", _env_file_encoding="utf-8")
    return config_settings
    # return Settings(app_version="1.2.3")
    # return config_settings.app_version == "1.2.3"
