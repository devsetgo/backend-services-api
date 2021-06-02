# -*- coding: utf-8 -*-
import unittest

from devsetgo_lib.file_functions import save_json
from starlette.testclient import TestClient

from src.core.gen_user import user_test_info
from src.main import app

client = TestClient(app)
directory_to__files: str = "data"


class Test(unittest.TestCase):
    def test_users_post_error(self):
        test_password = "testpassword"
        user_name = f"test-user-fail"

        test_data = {
            # "user_name": user_name,
            "password": test_password,
            "email": "bob@bob.com",
            "notes": "Gumbo beet greens corn soko endive gumbo gourd. ",
        }

        url = f"/api/v1/users/create"

        response = client.post(url, json=test_data)
        assert response.status_code == 422

    def test_users_post(self):
        test_user = user_test_info()
        save_json("test_data_test_user.json", test_user)
        url = f"/api/v1/users/create"

        response = client.post(url, json=test_user)
        assert response.status_code == 200
        data = response.json()

        user_data = {
            "id": data["id"],
            "user_name": data["user_name"],
            "password": test_user["password"],
        }

        save_json("test_data_users.json", user_data)

    def test_users_post_two(self):
        for _ in range(2):
            test_user = user_test_info()
            url = f"/api/v1/users/create"

            response = client.post(url, json=test_user)
            assert response.status_code == 200
