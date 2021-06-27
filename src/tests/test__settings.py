# -*- coding: utf-8 -*-

from fastapi.testclient import TestClient

from src import main
from src.settings import config_settings

client = TestClient(main.app)


# @mock.patch("settings.config_settings", return_value=Settings(app_version="1.2.3"))
def test_settings():

    assert config_settings.app_version != None
    assert config_settings.release_env == "test"
    assert config_settings.https_on != None
    assert config_settings.prometheus_on != None
    assert config_settings.loguru_retention != None
    assert config_settings.loguru_rotation != None
    assert config_settings.workers != None
    assert config_settings.db_name != None
    assert config_settings.db_dialect != None
    assert config_settings.db_url != None
    assert config_settings.db_user != None
    assert config_settings.db_pwd != None
