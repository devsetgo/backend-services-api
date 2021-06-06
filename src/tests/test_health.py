# -*- coding: utf-8 -*-
import unittest

from starlette.testclient import TestClient

from src.core.process_checks import get_platform
from src.main import app
from api.auth_routes import MANAGER
from .conftest import bearer_session

client = TestClient(app)

directory_to__files: str = "data"


def test_health_status():

    response = client.get(f"/api/health/status")
    assert response.status_code == 200


def test_health_system_info(bearer_session):
    # print(f"bear : {bearer_session}")
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.get(f"/api/health/system-info", headers=headers)
    assert response.status_code == 200


def test_health_processes(bearer_session):
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.get(f"/api/health/processes", headers=headers)
    assert response.status_code == 200


def test_configuration(bearer_session):
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.get(f"/api/health/configuration", headers=headers)
    assert response.status_code == 200


def test_get_platform():
    result = get_platform()
    assert result is not None
