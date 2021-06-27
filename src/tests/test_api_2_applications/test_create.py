# -*- coding: utf-8 -*-
# import unittest

import pytest
from starlette.testclient import TestClient
from devsetgo_lib.file_functions import save_json
from src.main import app

client = TestClient(app)


def test_users_post(bearer_session):
    
    test_data:dict={"appName": "test_app_1","description": "string"}
    url = f"api/v1/applications/create"
    headers = {"Authorization": "Bearer " + bearer_session}
    response = client.post(url, json=test_data, headers=headers)
    assert response.status_code == 201
    data = response.json()

    
    save_json("test_data_applications.json", data)

