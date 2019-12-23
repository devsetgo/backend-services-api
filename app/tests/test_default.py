# -*- coding: utf-8 -*-
import unittest

from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


class Test(unittest.TestCase):
    def test_index(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_joke(self):
        response = client.get("/joke")
        assert response.status_code == 200
        assert response.json is not None

    def test_information(self):
        response = client.get("/information")
        assert response.status_code == 200
