# -*- coding: utf-8 -*-

import pytest
from starlette.testclient import TestClient

from src.main import app
from src.settings import Settings, get_settings, config_settings


def get_settings_override() -> Settings:
    return Settings(release_env="test")


@pytest.fixture(autouse=True)
def override_settings() -> None:
    app.dependency_overrides[get_settings] = get_settings_override


@pytest.fixture(scope="session")
def bearer_session():
    client = TestClient(app)
    data = {
        "username": config_settings.admin_user_name,
        "password": config_settings.admin_password,
    }
    response = client.post("/api/v1/auth/login", data=data)
    token_data = response.json()
    return token_data["access_token"]
