# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient
import pytest
from src import main
from src.settings import config_settings,Settings

client = TestClient(main.app)


def test_settings():
    assert config_settings.app_version == "1.2.3"
    assert config_settings.release_env != None
    assert config_settings.https_on != None
    assert config_settings.prometheus_on != None
    assert config_settings.sqlalchemy_database_uri != None
    assert config_settings.loguru_retention != None
    assert config_settings.loguru_rotation != None
    assert config_settings.workers != None