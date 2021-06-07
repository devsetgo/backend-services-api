# -*- coding: utf-8 -*-

from devsetgo_lib.file_functions import open_json
from starlette.testclient import TestClient

from src.main import app


client = TestClient(app)

directory_to__files: str = "data"

test_data_users = "test_data_users.json"
test_data_test_user = "test_data_test_user.json"


def test_user_password(bearer_session):
    user_id = open_json(test_data_users)
    test_data = {"user_name": user_id["userName"], "password": user_id["password"]}
    url = f"/api/v1/users/check-pwd"
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.post(url, data=test_data, headers=headers)
    result = response.json()
    assert response.status_code == 201
    assert result["result"] == True


def test_users_count(bearer_session):
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.get(f"api/v1/users/list/count", headers=headers)
    assert response.status_code == 200


def test_users_list_params(bearer_session):
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.get(
        f"api/v1/users/list?qty=100&offset=1&active=true", headers=headers
    )
    assert response.status_code == 200


def test_users_list_offset(bearer_session):
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.get(f"api/v1/users/list?qty=2", headers=headers)

    test_offset_1 = response.json()
    test_user_1 = test_offset_1["users"][1]
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.get(f"api/v1/users/list?qty=2&offset=1", headers=headers)
    test_offset_2 = response.json()
    test_user_2 = test_offset_2["users"][0]
    assert response.status_code == 200
    assert test_user_1["id"] == test_user_2["id"]


def test_users_list_param_none(bearer_session):
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.get(f"/api/v1/users/list", headers=headers)
    assert response.status_code == 200


def test_users_list_options(bearer_session):
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.get(f"/api/v1/users/list?qty=2&active=true", headers=headers)
    assert response.status_code == 200


def test_users_list_param_all(bearer_session):
    data = open_json(test_data_test_user)
    a = data["userName"]
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.get(
        f"/api/v1/users/list?active=true&username={a}", headers=headers
    )
    assert response.status_code == 200


def test_users_id(bearer_session):
    user_id = open_json(test_data_users)
    uid = user_id["id"]
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.get(f"/api/v1/users/{uid}", headers=headers)
    state = response.status_code
    assert state is 200
    assert response.json() is not None


def test_users_put_status_deactivate(bearer_session):
    user_id = open_json(test_data_users)
    test_data = {"id": user_id["id"], "isActive": False}
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.put(f"/api/v1/users/status", json=test_data, headers=headers)
    assert response.status_code == 200


def test_users_put_status_activate(bearer_session):
    user_id = open_json(test_data_users)
    test_data = {"id": user_id["id"], "isActive": True}
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.put(f"/api/v1/users/status", json=test_data, headers=headers)
    assert response.status_code == 200
