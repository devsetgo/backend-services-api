# -*- coding: utf-8 -*-
import asyncio
import json
import uuid

from fastapi import APIRouter, File, HTTPException, Path, Query, UploadFile
from loguru import logger

from com_lib.simple_functions import get_current_datetime
from db_setup import app_config, database
from endpoints.configuration.models import AppConfigurationBase, ConfigUpdate

router = APIRouter()


@router.get("/list", tags=["configuration"])
async def configuration_list(
    qty: int = Query(
        None,
        title="Quanity",
        description="Records to return (max 500)",
        ge=1,
        le=500,
        alias="qty",
    ),
    offset: int = Query(
        None, title="Offset", description="Offset increment", ge=0, alias="offset"
    ),
    is_active: bool = Query(None, title="by active status", alias="active"),
) -> dict:

    """
    list of configuarations

    Keyword Arguments:

        qty {int} -- [description] 100 returned results is default, maximum is 500
        offset {int} -- [description] 0 seconds default
        Active {bool} -- [description] no default as not required, must be Active=true or false if used

    Returns:
        dict -- [description]
    """

    if qty is None:
        qty: int = 100

    if offset is None:
        offset: int = 0

    # Fetch multiple rows
    if is_active is not None:
        query = (
            app_config.select()
            .where(app_config.c.is_active == is_active)
            .order_by(app_config.c.date_created)
            .limit(qty)
            .offset(offset)
        )
        db_result = await database.fetch_all(query)

        count_query = (
            app_config.select()
            .where(app_config.c.is_active == is_active)
            .order_by(app_config.c.date_created)
        )
        total_count = await database.fetch_all(count_query)

    else:

        query = (
            app_config.select()
            .order_by(app_config.c.date_created)
            .limit(qty)
            .offset(offset)
        )
        db_result = await database.fetch_all(query)
        count_query = app_config.select().order_by(app_config.c.date_created)
        total_count = await database.fetch_all(count_query)

    result_set = []
    for r in db_result:
        # iterate through data and return simplified data set
        configuration_data = {
            "config_id": r["config_id"],
            "config_name": r["config_name"],
            "config_version": r["config_version"],
            "description": r["description"],
            "configuration_data": r["configuration_data"],
            "date_created": r["date_created"],
            "date_updated": r["date_updated"],
            "is_active": r["is_active"],
        }
        result_set.append(configuration_data)

    result = {
        "parameters": {
            "returned_results": len(result_set),
            "qty": qty,
            "total_count": len(total_count),
            "offset": offset,
            "filter_active_status": is_active,
        },
        "configuaration": result_set,
    }
    return result


@router.get(
    "/list/count",
    tags=["configuration"],
    response_description="Get count of configuarations",
    responses={
        404: {"description": "Operation forbidden"},
        500: {"description": "Mommy!"},
    },
)
async def configuarations_list_count(
    is_active: bool = Query(None, title="by active status", alias="active"),
) -> dict:
    """
    Count of configuarations in the database

    Keyword Arguments:

        Active {bool} -- [description] no default as not required, must be Active=true or false if used

    Returns:
        dict -- [description]
    """

    try:
        # Fetch multiple rows
        if is_active is not None:
            query = app_config.select().where(app_config.c.is_active == is_active)
            x = await database.fetch_all(query)
        else:
            query = app_config.select()
            x = await database.fetch_all(query)

        result = {"count": len(x)}
        return result
    except Exception as e:
        logger.error(f"Critical Error: {e}")


@router.get(
    "/{config_name}",
    tags=["configuration"],
    response_description="Get configuration information",
)
async def get_confg_name(
    config_name: str = Path(
        ..., title="The configuration id to be searched for", alias="config_name"
    ),
) -> dict:
    """
    configuration information for requested UUID

    Keyword Arguments:
        config_name {str} -- [description] unique name of configuration required

    Returns:
        dict -- [description]
    """

    try:
        # Fetch single row
        query = app_config.select().where(app_config.c.config_name == config_name)
        db_result = await database.fetch_one(query)

        config_data = db_result
        #  {
        #     "config_id": db_result["config_id"],
        #     "config_name": db_result["config_name"],
        #     "first_name": db_result["first_name"],
        #     "last_name": db_result["last_name"],
        #     "company": db_result["company"],
        #     "title": db_result["title"],
        #     "address": db_result["address"],
        #     "city": db_result["city"],
        #     "country": db_result["country"],
        #     "postal": db_result["postal"],
        #     "email": db_result["email"],
        #     "website": db_result["website"],
        #     "description": db_result["description"],
        #     "date_created": db_result["date_created"],
        #     "date_updated": db_result["date_updated"],
        #     "is_active": db_result["is_active"],
        # }
        return config_data

    except Exception as e:
        logger.error(f"Critical Error: {e}")


@router.get(
    "/{config_id}",
    tags=["configuration"],
    response_description="Get configuration information",
)
async def get_confg_id(
    config_id: str = Path(
        ..., title="The configuration id to be searched for", alias="config_id"
    ),
) -> dict:
    """
    configuration information for requested UUID

    Keyword Arguments:
        config_name {str} -- [description] unique name of configuration required

    Returns:
        dict -- [description]
    """

    try:
        # Fetch single row
        query = app_config.select().where(app_config.c.config_id == config_id)
        db_result = await database.fetch_one(query)

        config_data = db_result

        return config_data

    except Exception as e:
        logger.error(f"Critical Error: {e}")


@router.put(
    "/update/{config_name}",
    tags=["configuration"],
    response_description="The confguration",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def update_config_name(
    *,
    config_update: ConfigUpdate,
    config_name: str = Path(
        ..., title="The configuration to be deactivated", alias="config_name"
    ),
) -> dict:
    """
    Deactivate a specific configuration UUID

    Keyword Arguments:
        config_id {str} -- [description] UUID of config_id property required

    Returns:
        dict -- [description]
    """
    config_information = {
        "date_updated": get_current_datetime(),
    }

    try:
        # Fetch single row
        query = app_config.update().where(app_config.c.config_name == config_name)
        values = config_information
        result = await database.execute(query, values)
        return result
    except Exception as e:
        logger.error(f"Critical Error: {e}")


@router.put(
    "/deactivate/{config_name}",
    tags=["configuration"],
    response_description="Deactivated",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def deactivate_config_name(
    *,
    config_name: str = Path(
        ..., title="The configuration name to be deactivated", alias="config_name"
    ),
) -> dict:
    """
    Deactivate a specific config UUID

    Keyword Arguments:
        config_id {str} -- [description] name of config_name property required

    Returns:
        dict -- [description]
    """
    config_information = {"is_active": False, "date_updated": get_current_datetime()}

    try:
        # Fetch single row
        query = app_config.update().where(app_config.c.config_name == config_name)
        values = config_information
        result = await database.execute(query, values)
        return result
    except Exception as e:
        logger.error(f"Critical Error: {e}")


@router.put(
    "/deactivate/{config_id}",
    tags=["configuration"],
    response_description="Deactivated",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def deactivate_config_id(
    *,
    config_id: str = Path(
        ..., title="The configuration ID to be deactivated", alias="config_id"
    ),
) -> dict:
    """
    Deactivate a specific config UUID

    Keyword Arguments:
        config_id {str} -- [description] UUID of config_id property required

    Returns:
        dict -- [description]
    """
    config_information = {"is_active": False, "date_updated": get_current_datetime()}

    try:
        # Fetch single row
        query = app_config.update().where(app_config.c.config_id == config_id)
        values = config_information
        result = await database.execute(query, values)
        return result
    except Exception as e:
        logger.error(f"Critical Error: {e}")


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
        "date_created": get_current_datetime(),
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

        if "UNIQUE constraint" in str(e):
            detail = f"config_name must be unique"
            logger.critical(f"ERROR 400: {detail}")
            raise HTTPException(status_code=400, detail=detail)
        else:
            logger.error(f"Critical Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))
