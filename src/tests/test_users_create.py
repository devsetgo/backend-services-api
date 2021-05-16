# -*- coding: utf-8 -*-
import unittest

from starlette.testclient import TestClient

from src.core.file_functions import save_json
from src.core.gen_user import user_test_info
from src.main import app

client = TestClient(app)
directory_to__files: str = "data"


class Test(unittest.TestCase):
    def test_users_post_error(self):
        test_password = "testpassword"
        user_name = f"test-user-fail"

        test_data = {
            "user_name": user_name,
            # "firstName": "string",
            "last_name": "string",
            "password": test_password,
            "title": "string",
            "company": "string",
            "address": "string",
            "city": "string",
            "country": "string",
            "phone": "string",
            "postal": "string",
            "email": "string",
            "website": "string",
            "description": "string",
        }

        url = f"/api/v1/users/create/"

        response = client.post(url, json=test_data)
        assert response.status_code == 422

    def test_users_post(self):
        test_user = user_test_info()
        save_json("test_data_test_user.json", test_user)
        url = f"/api/v1/users/create/?delay=1"

        response = client.post(url, json=test_user)
        assert response.status_code == 200
        data = response.json()

        user_data = {
            "user_id": data["user_id"],
            "user_name": data["user_name"],
            "password": test_user["password"],
        }

        save_json("test_data_users.json", user_data)

    def test_users_post_two(self):
        for _ in range(2):
            test_user = user_test_info()
            url = f"/api/v1/users/create/?delay=1"

            response = client.post(url, json=test_user)
            assert response.status_code == 200
