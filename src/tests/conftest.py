# -*- coding: utf-8 -*-

import pytest
from starlette.testclient import TestClient

from src.main import app
from src.settings import Settings, get_settings, settings

client = TestClient(app)


# @pytest.fixture(scope="session")
# def update_settings():
#     settings = Settings(_env_file=".env_test", _env_file_encoding="utf-8")


def get_settings_override() -> Settings:
    return Settings(release_env="test")


@pytest.fixture(autouse=True)
def override_settings() -> None:
    app.dependency_overrides[get_settings] = get_settings_override
    print(settings)


@pytest.fixture(scope="session")
def bearer_session():
    # client.get()
    data = {"username": "johndoe", "password": "secret"}
    response = client.post("/api/v1/auth/login", data=data)
    token_data = response.json()
    return token_data["access_token"]
