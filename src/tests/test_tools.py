# -*- coding: utf-8 -*-
import unittest
from pathlib import Path

from starlette.testclient import TestClient

from src.main import app

client = TestClient(app)

directory_to__files: str = "data"


class Test(unittest.TestCase):
    # xml endpoint test
    def test_xml_four_hundred(self):
        file_directory = f"{directory_to__files}/testfiles"
        directory_path = Path.cwd().joinpath(file_directory)
        file_path = f"{directory_path}/test_sample.json"

        url = f"/api/v1/tools/xml-json"
        files = {"myfile": open(file_path, "r")}
        response = client.post(url, files=files)
        assert response.status_code == 400

    def test_xml(self):
        file_directory = f"{directory_to__files}/testfiles"
        directory_path = Path.cwd().joinpath(file_directory)
        file_path = f"{directory_path}/test_sample.xml"

        url = f"/api/v1/tools/xml-json"
        files = {"myfile": open(file_path, "r")}
        response = client.post(url, files=files)
        assert response.status_code == 200

    def test_xml_error(self):
        file_directory = f"{directory_to__files}/testfiles"
        directory_path = Path.cwd().joinpath(file_directory)
        file_path = f"{directory_path}/test_sample_bad.xml"

        url = f"/api/v1/tools/xml-json"
        files = {"myfile": open(file_path, "r")}
        response = client.post(url, files=files)
        assert response.status_code == 400

    # json endpoint test
    def test_json_four_hundred(self):
        file_directory = f"{directory_to__files}/testfiles"
        directory_path = Path.cwd().joinpath(file_directory)
        file_path = f"{directory_path}/test_sample.xml"

        url = f"/api/v1/tools/json-xml"
        files = {"myfile": open(file_path, "r")}
        response = client.post(url, files=files)
        assert response.status_code == 400

    def test_json(self):
        file_directory = f"{directory_to__files}/testfiles"
        directory_path = Path.cwd().joinpath(file_directory)
        file_path = f"{directory_path}/test_sample.json"

        url = f"/api/v1/tools/json-xml"
        files = {"myfile": open(file_path, "r")}
        response = client.post(url, files=files)
        assert response.status_code == 200

    def test_json_error(self):
        file_directory = f"{directory_to__files}/testfiles"
        directory_path = Path.cwd().joinpath(file_directory)
        file_path = f"{directory_path}/test_sample_bad.json"

        url = f"/api/v1/tools/json-xml"
        files = {"myfile": open(file_path, "r")}
        response = client.post(url, files=files)
        assert response.status_code == 400
