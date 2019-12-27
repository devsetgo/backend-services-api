# -*- coding: utf-8 -*-
import unittest

from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


class Test(unittest.TestCase):
    def test_silly_make_one_delay(self):

        response = client.get("/api/v1/silly-users/make-one?delay=1")
        assert response.status_code == 200

    def test_silly_make_one(self):

        response = client.get("/api/v1/silly-users/make-one")
        assert response.status_code == 200

    def test_silly_list_qty_delay(self):

        response = client.get("/api/v1/silly-users/list?qty=3&delay=1")
        assert response.status_code == 200

    def test_silly_list(self):

        response = client.get("/api/v1/silly-users/list?qty=1")
        assert response.status_code == 200

    def test_silly_list_error(self):

        response = client.get("/api/v1/silly-users/list")
        assert response.status_code == 422

    def test_silly_list_error_delay(self):

        response = client.get("/api/v1/silly-users/list?delay=122")
        assert response.status_code == 422
