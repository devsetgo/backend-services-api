# -*- coding: utf-8 -*-

from devsetgo_lib.file_functions import save_json
from starlette.testclient import TestClient

from src.core.gen_user import user_test_info
from src.main import app


client = TestClient(app)
directory_to__files: str = "data"


def test_users_post_error(bearer_session):
    test_password = "testpassword"
    user_name = f"test-user-fail"
    test_data = {
        "user_name": user_name,
        "password": test_password,
        "password": f"{test_password}1",
        "email": "bob@bob.com",
        "notes": "Gumbo beet greens corn soko endive gumbo gourd. ",
    }
    url = f"/api/v1/users/create"
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.post(url, json=test_data, headers=headers)
    assert response.status_code == 422


def test_users_post_error_email(bearer_session):
    test_password = "testpassword"
    user_name = f"test-user-fail"
    test_data = {
        "userName": user_name,
        "password": test_password,
        "passwordTwo": test_password,
        "email": "bob@bob",
        "notes": "Gumbo beet greens corn soko endive gumbo gourd. ",
    }
    url = f"/api/v1/users/create"
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.post(url, json=test_data, headers=headers)
    assert response.status_code == 422


def test_users_post(bearer_session):
    test_user = user_test_info()
    save_json("test_data_test_user.json", test_user)
    url = f"/api/v1/users/create"
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.post(url, json=test_user, headers=headers)
    assert response.status_code == 201
    data = response.json()
    user_data = {
        "id": data["id"],
        "userName": data["user_name"],
        "password": test_user["password"],
    }
    save_json("test_data_users.json", user_data)


def test_users_post_two(bearer_session):
    for p in range(2):
        test_user = user_test_info()
        url = f"/api/v1/users/create"
        headers = {"Authorization": "Bearer " + bearer_session}
        response = client.post(url, json=test_user, headers=headers)
        save_json(f"test_user_{p}.json", test_user)
        assert response.status_code == 201
