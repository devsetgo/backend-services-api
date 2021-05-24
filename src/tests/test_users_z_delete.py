# -*- coding: utf-8 -*-
import unittest
import uuid
from starlette.testclient import TestClient

from devsetgo_lib.file_functions import open_json
from src.main import app

client = TestClient(app)

directory_to__files: str = "data"


class Test(unittest.TestCase):
    def test_users_delete(self):
        user_id = open_json("test_data_users.json")
        response = client.delete(f"/api/v1/users/{user_id['id']}")
        assert response.status_code == 200

    def test_users_delete_four_zero_four(self):

        response = client.delete(f"/api/v1/users/{uuid.uuid4()}")
        assert response.status_code == 404

    def test_users_method_fail(self):
        response = client.post(f"/api/v1/users/{uuid.uuid4()}")
        assert response.status_code == 405
