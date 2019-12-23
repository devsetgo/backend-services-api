# -*- coding: utf-8 -*-
import json
import asyncio
import uuid
from fastapi import APIRouter
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from loguru import logger
from endpoints.configuration.models import AppConfigurationBase
from com_lib.simple_functions import get_current_datetime
from db_setup import database
from db_setup import app_config

router = APIRouter()


@router.get("/", tags=["configuration"])
async def get_configuration() -> dict:
    """
    GET configuration for application

    Returns:
        dict -- [a bunch of data]
    """
    qty = 100
    offset = 0
    query = (
        app_config.select().order_by(app_config.c.date_create).limit(qty).offset(offset)
    )
    db_result = await database.fetch_all(query)
    result: dict = {"configuration": "has one"}
    return db_result


@router.post("/create-config", tags=["configuration"])
async def create_configuration(new_config: AppConfigurationBase) -> dict:

    value = new_config.dict()
    if value["configuration"] is None:
        detail = f"'configuration_data' cannot be empty"
        raise HTTPException(status_code=400, detail=detail)

    config_data = json.dumps(value["configuration"])
    print(config_data)
    create_new_config = {
        "config_id": str(uuid.uuid4()),
        "config_name": value["config_name"],
        "config_version": value["config_version"],
        "date_create": get_current_datetime(),
        "date_updated": get_current_datetime(),
        "is_active": True,
        "configuration_data": value["configuration"],
    }
    try:
        query = app_config.insert()
        values = create_new_config
        await database.execute(query, values)

        result = {
            "config_id": create_new_config["config_id"],
            "config_name": value["config_name"],
        }
        return result
    except Exception as e:
        logger.error(f"Critical Error: {e}")
        if "UNIQUE constraint" in str(e):
            detail = f"config_name must be unique"
            logger.critical(f"ERROR 400: {detail}")
            raise HTTPException(status_code=400, detail=detail)
