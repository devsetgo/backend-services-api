# -*- coding: utf-8 -*-
import unittest

from starlette.testclient import TestClient

from app.com_lib.file_functions import save_json, open_json
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
        test_config_1 = test_offset_1["configuaration"][1]
        response = client.get(f"api/v1/configuration/list?qty=2&offset=1")
        test_offset_2 = response.json()
        test_config_2 = test_offset_2["configuaration"][0]
        assert response.status_code == 200
        assert test_config_1["config_id"] == test_config_2["config_id"]

    def test_config_list_param_none(self):

        response = client.get(f"/api/v1/configuration/list")
        assert response.status_code == 200

    def test_config_list_options(self):

        response = client.get(f"api/v1/configuration/list?qty=2&active=true")
        assert response.status_code == 200

    def test_config_count(self):

        response = client.get(f"api/v1/configuration/list/count")
        data = response.json()
        assert response.status_code == 200
        assert data["count"] is not 0

    def test_config_count_option(self):

        response = client.get(f"api/v1/configuration/list/count?active=true")
        data = response.json()
        assert response.status_code == 200
        assert data["count"] is not 0

    def test_config_item_id(self):
        test_data = open_json("test_data_config.json")
        config_id = test_data["config_id"]
        response = client.get(f"api/v1/configuration/item?config_id={config_id}")
        data = response.json()
        assert response.status_code == 200
        assert data["config_name"] is not None

    def test_config_item_name(self):
        test_data = open_json("test_data_config.json")
        config_name = test_data["config_name"]
        response = client.get(f"api/v1/configuration/item?config_name={config_name}")
        data = response.json()
        assert response.status_code == 200
        assert data["config_name"] is not None

    def test_config_item_name_id_error(self):
        test_data = open_json("test_data_config.json")
        config_id = test_data["config_id"]
        config_name = test_data["config_name"]
        response = client.get(
            f"api/v1/configuration/item?config_id={config_id}&config_name={config_name}"
        )
        data = response.json()
        assert response.status_code == 400
        assert data["detail"] == "Either config_id or config_name can be used."

    def test_config_item_no_name_id_error(self):
        response = client.get(f"api/v1/configuration/item")
        data = response.json()
        assert response.status_code == 400
        assert data["detail"] == "Either config_id or config_name must be used."

    def test_config_item_four_zero_four(self):
        response = client.get(f"api/v1/configuration/item?config_id=1")
        data = response.json()
        assert response.status_code == 404
        # assert data['detail'] == "Either config_id or config_name must be used."

    def test_config_update_id(self):
        send_data = {
            "configuration_data": {"this": "and", "and": "that"},
            "config_version": "string",
            "description": "string",
        }
        test_data = open_json("test_data_config.json")
        config_id = test_data["config_id"]
        url = f"api/v1/configuration/update?config_id={config_id}"
        response = client.put(url, json=send_data)
        data = response.json()
        assert response.status_code == 200
        # assert data['detail'] == "Either config_id or config_name must be used."

    def test_config_update_name(self):
        send_data = {
            "configuration_data": {"this": "and", "and": "that"},
            "config_version": "string",
            "description": "string",
        }
        test_data = open_json("test_data_config.json")
        config_name = test_data["config_name"]
        url = f"api/v1/configuration/update?config_name={config_name}"
        response = client.put(url, json=send_data)
        data = response.json()
        assert response.status_code == 200
        # assert data['detail'] == "Either config_id or config_name must be used."

    def test_config_update_id_no_config(self):
        send_data = {
            "configuration_data": {},
            "config_version": "string",
            "description": "string",
        }
        test_data = open_json("test_data_config.json")
        config_id = test_data["config_id"]
        url = f"api/v1/configuration/update?config_id={config_id}"
        response = client.put(url, json=send_data)
        data = response.json()
        assert response.status_code == 400
        # assert data['detail'] == "Either config_id or config_name must be used."



    def test_config_update_name_id_error(self):
        send_data = {
            "configuration_data": {"this": "and", "and": "that"},
            "config_version": "string",
            "description": "string",
        }
        test_data = open_json("test_data_config.json")
        config_name = test_data["config_name"]
        config_id = test_data["config_id"]
        url = f"api/v1/configuration/update?config_name={config_name}&config_id={config_id}"
        response = client.put(url, json=send_data)
        data = response.json()
        assert response.status_code == 400
        assert data["detail"] == "Either config_id or config_name can be used."

    def test_config_update_no_name_id_error(self):
        send_data = {
            "configuration_data": {"this": "and", "and": "that"},
            "config_version": "string",
            "description": "string",
        }
        url = f"api/v1/configuration/update"
        response = client.put(url, json=send_data)
        data = response.json()
        assert response.status_code == 400
        assert data["detail"] == "Either config_id or config_name must be used."


    def test_config_active_status_id(self):
        test_data = open_json("test_data_config.json")
        config_name = test_data["config_name"]
        config_id = test_data["config_id"]
        url = f"api/v1/configuration/active-status?config_id={config_id}"
        response = client.put(url)
        data = response.json()
        assert response.status_code == 200

    def test_config_active_status_name(self):
        test_data = open_json("test_data_config.json")
        config_name = test_data["config_name"]
        config_id = test_data["config_id"]
        url = f"api/v1/configuration/active-status?config_name={config_name}"
        response = client.put(url)
        data = response.json()
        assert response.status_code == 200
        

    def test_config_active_status_name_active(self):
        test_data = open_json("test_data_config.json")
        config_name = test_data["config_name"]
        config_id = test_data["config_id"]
        url = f"api/v1/configuration/active-status?config_name={config_name}&active=true"
        response = client.put(url)
        data = response.json()
        assert response.status_code == 200


    def test_config_active_status_name_deactive(self):
        test_data = open_json("test_data_config.json")
        config_name = test_data["config_name"]
        config_id = test_data["config_id"]
        url = f"api/v1/configuration/active-status?config_name={config_name}&active=false"
        response = client.put(url)
        data = response.json()
        assert response.status_code == 200

    def test_config_active_status_name_id_error(self):
        test_data = open_json("test_data_config.json")
        config_name = test_data["config_name"]
        config_id = test_data["config_id"]
        url = f"api/v1/configuration/active-status?config_name={config_name}&config_id={config_id}"
        response = client.put(url)
        data = response.json()
        assert response.status_code == 400

    def test_config_active_status_no_id_name_error(self):
        url = f"api/v1/configuration/active-status"
        response = client.put(url)
        data = response.json()
        assert response.status_code == 400

    def test_config_active_status_id_error(self):
        
        config_id = '1'
        url = f"api/v1/configuration/active-status?config_id={config_id}"
        response = client.put(url)
        assert response.status_code == 404