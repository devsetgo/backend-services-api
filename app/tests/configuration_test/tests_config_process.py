# -*- coding: utf-8 -*-
import unittest

from starlette.testclient import TestClient

from app.com_lib.file_functions import save_json
from app.main import app

client = TestClient(app)
directory_to__files: str = "data"


class Test(unittest.TestCase):
    def test_config_list_params(self):

        response = client.get(f"api/v1/configuration/list?qty=100&offset=1&active=true")
        assert response.status_code == 200

    def test_config_list_offset(self):

        response = client.get(f"api/v1/configuration/list?qty=2")

        test_offset_1 = response.json()
        test_user_1 = test_offset_1["users"][1]
        response = client.get(f"api/v1/configuration/list?qty=2&offset=1")
        test_offset_2 = response.json()
        test_user_2 = test_offset_2["users"][0]
        assert response.status_code == 200
        assert test_user_1["config_id"] == test_user_2["user_id"]

    def test_config_list_param_none(self):

        response = client.get(f"/api/v1/configuration/list")
        assert response.status_code == 200

    def test_config_list_options(self):

        response = client.get(f"api/v1/configuration/list?qty=2&active=true")
        assert response.status_code == 200
