# -*- coding: utf-8 -*-
import secrets
import uuid

from starlette.testclient import TestClient

from src.main import app

client = TestClient(app)
directory_to__files: str = "data"

test_data = {
    "user_name": "bob",
    "password": "1234",
    "passwordTwo": "1234",
    "email": "bob@bob.com",
    "notes": "Gumbo beet greens corn soko endive gumbo gourd. ",
    "isActive": False,
}

headers = {"Authorization": "Bearer " + secrets.token_urlsafe(8)}


def test_users_list_auth_fail():

    url = f"/api/v1/users/create"
    response = client.get(url, json=test_data, headers=headers)
    assert response.status_code == 401


def test_users_count_auth_fail():
    url = f"/api/v1/users/list"
    response = client.get(url, headers=headers)
    assert response.status_code == 401


def test_users_userid_auth_fail():
    url = f"/api/v1/users/list/count"
    response = client.get(url, headers=headers)
    assert response.status_code == 401


def test_users_user_status_auth_fail():
    url = f"/api/v1/users/status"
    response = client.put(url, json=test_data, headers=headers)
    assert response.status_code == 401


def test_users_user_delete_auth_fail():
    url = f"/api/v1/users/{uuid.uuid4()}"
    response = client.delete(url, json=test_data, headers=headers)
    assert response.status_code == 401


def test_users_create_auth_fail():
    url = f"/api/v1/users/create"
    response = client.post(url, json=test_data, headers=headers)
    assert response.status_code == 401


def test_users_pwd_auth_fail():
    url = f"/api/v1/users/create"
    response = client.get(url, json=test_data, headers=headers)
    assert response.status_code == 401
