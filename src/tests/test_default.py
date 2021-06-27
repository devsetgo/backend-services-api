# -*- coding: utf-8 -*-
# import unittest

import pytest
from starlette.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200


def test_information():
    response = client.get("/info")
    assert response.status_code == 200


def test_metrics():
    response = client.get("/api/health/metrics")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_user():
    from src.data_base.users import default_user

    await default_user()


@pytest.mark.asyncio
async def test_default_user_fail():
    from src.data_base.users import default_user

    await default_user()
