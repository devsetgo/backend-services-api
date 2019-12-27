# -*- coding: utf-8 -*-
import asyncio
import json
import uuid

from fastapi import APIRouter, File, HTTPException, Path, Query, UploadFile
from loguru import logger

from com_lib.simple_functions import get_current_datetime
from db_setup import app_config, database
from endpoints.configuration.models import AppConfigurationBase, ConfigUpdate


async def fetch_one_db(query):

    result = await database.fetch_one(query)
    return result


async def fetch_all_db(query):

    result = await database.fetch_all(query)
    return result


async def execute_one_db(query, values: dict):

    result = await database.execute(query, values)
    return result
