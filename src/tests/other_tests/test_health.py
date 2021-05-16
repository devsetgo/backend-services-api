# -*- coding: utf-8 -*-
import unittest

from starlette.testclient import TestClient

from app.health.checks import get_platform
from app.main import app

client = TestClient(app)

directory_to__files: str = "data"


class Test(unittest.TestCase):
    def test_health_status(self):
        response = client.get(f"/api/health/")
        assert response.status_code == 200

    def test_health_system_info(self):

        response = client.get(f"/api/health/system-info")
        assert response.status_code == 200

    def test_health_processes(self):

        response = client.get(f"/api/health/processes")
        assert response.status_code == 200

    def test_get_platform(self):
        result = get_platform()
        assert result is not None
