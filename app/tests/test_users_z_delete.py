# -*- coding: utf-8 -*-
import unittest

from starlette.testclient import TestClient

from app.com_lib.file_functions import open_json
from app.main import app

client = TestClient(app)

directory_to__files: str = "data"


class Test(unittest.TestCase):
    def test_users_delete_delay(self):
        user_id = open_json("test_data_users.json")

        response = client.delete(f"/api/v1/users/{user_id['user_id']}?delay=1")
        assert response.status_code == 200
