# -*- coding: utf-8 -*-
import unittest
from random import randint

from starlette.testclient import TestClient

from app.com_lib.file_functions import save_json
from app.main import app

client = TestClient(app)
directory_to__files: str = "data"


class Test(unittest.TestCase):
    def test_config_post_error(self):

        test_data = {
            "config_name": f"test_fail-{randint(0,10000)}-{randint(0,10000)}",
            "configuration_data": {},
            "config_version": "string",
            "description": "string",
        }

        url = f"/api/v1/configuration/create-config"

        response = client.post(url, json=test_data)
        assert response.status_code == 400

    def test_users_post(self):

        url = f"/api/v1/configuration/create-config"
        test_data = {
            "config_name": f"test_pass-{randint(0,10000)}-{randint(0,10000)}",
            "configuration_data": {"first": "things", "things": "first"},
            "config_version": "1.23",
            "description": "first things first",
        }

        response = client.post(url, json=test_data)
        r = response.json()
        assert response.status_code == 200

        resp_data = {
            "config_id": r["config_id"],
            "config_name": r["config_name"],
            "configuration_data": {"first": "things", "things": "first"},
            "config_version": "1",
            "description": "first things first",
        }

        save_json("test_data_config.json", resp_data)

    def test_users_post_two(self):
        test_data = {
            "config_name": f"test_pass-{randint(0,10000)}-{randint(0,10000)}",
            "configuration_data": {"first": "things", "things": "first"},
            "config_version": "2",
            "description": "first things first",
        }
        url = f"/api/v1/configuration/create-config"

        response = client.post(url, json=test_data)
        assert response.status_code == 200

    def test_users_post_data_twice(self):
        test_data = {
            "config_name": f"test_pass-1",
            "configuration_data": {"first": "things", "things": "first"},
            "config_version": "2",
            "description": "first things first",
        }
        url = f"/api/v1/configuration/create-config"

        response_1 = client.post(url, json=test_data)
        response_2 = client.post(url, json=test_data)
        assert response_2.status_code == 400
