# -*- coding: utf-8 -*-
import uuid

from devsetgo_lib.file_functions import open_json
from starlette.testclient import TestClient

from src.main import app


client = TestClient(app)

directory_to__files: str = "data"


def test_users_delete(bearer_session):
    user_id = open_json("test_data_users.json")
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.delete(f"/api/v1/users/{user_id['id']}", headers=headers)
    assert response.status_code == 200


def test_users_delete_four_zero_four(bearer_session):
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.delete(f"/api/v1/users/{uuid.uuid4()}", headers=headers)
    assert response.status_code == 404


def test_users_method_fail(bearer_session):
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.post(f"/api/v1/users/{uuid.uuid4()}", headers=headers)
    assert response.status_code == 405
