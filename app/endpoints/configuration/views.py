# -*- coding: utf-8 -*-
import json
import uuid

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from loguru import logger

from com_lib.simple_functions import get_current_datetime
from db_setup import app_config
from endpoints.configuration.crud_ops import execute_one_db
from endpoints.configuration.crud_ops import fetch_all_db
from endpoints.configuration.crud_ops import fetch_one_db
from endpoints.configuration.models import AppConfigurationBase
from endpoints.configuration.models import ConfigUpdate

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

        db_result = await fetch_all_db(query)

        count_query = (
            app_config.select()
            .where(app_config.c.is_active == is_active)
            .order_by(app_config.c.date_created)
        )

        total_count = await fetch_all_db(count_query)

    else:

        query = (
            app_config.select()
            .order_by(app_config.c.date_created)
            .limit(qty)
            .offset(offset)
        )
        db_result = await fetch_all_db(query)
        count_query = app_config.select().order_by(app_config.c.date_created)
        total_count = await fetch_all_db(count_query)

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
            "revision": r["revision"],
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

    # Fetch multiple rows
    if is_active is not None:
        query = app_config.select().where(app_config.c.is_active == is_active)
        x = await fetch_all_db(query)
    else:
        query = app_config.select()
        x = await fetch_all_db(query)
    logger.info(f"Cofiguration list queried")
    result = {"count": len(x)}
    return result


@router.get(
    "/item",
    tags=["configuration"],
    response_description="Get configuration information",
)
async def get_confg_id(
    config_id: str = Query(
        None, title="The configuration id to be searched for", alias="config_id"
    ),
    config_name: str = Query(
        None, title="The configuration id to be searched for", alias="config_name"
    ),
) -> dict:
    """
    configuration information for requested UUID

    Keyword Arguments:
        config_name {str} -- [description] unique name of configuration required

    Returns:
        dict -- [description]
    """

    if config_id is None and config_name is None:
        detail = f"Either config_id or config_name must be used."
        logger.error(f"Error: {detail}")
        raise HTTPException(status_code=400, detail=detail)
    elif config_id is not None and config_name is not None:
        detail = f"Either config_id or config_name can be used."
        logger.error(f"Error: {detail}")
        raise HTTPException(status_code=400, detail=detail)

    # Fetch single row
    if config_name is not None:
        query = app_config.select().where(app_config.c.config_name == config_name)
    if config_id is not None:
        query = app_config.select().where(app_config.c.config_id == config_id)

    db_result = await fetch_one_db(query)

    if db_result is None:
        # return error if empty results
        detail = f"No results match query criteria"
        logger.error(f"Error: {detail} {db_result}")
        raise HTTPException(status_code=404, detail=detail)

    return db_result


@router.put(
    "/update",
    tags=["configuration"],
    response_description="The confguration",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def update_config(
    *,
    config_update: ConfigUpdate,
    config_id: str = Query(
        None, title="The configuration id to be searched for", alias="config_id"
    ),
    config_name: str = Query(
        None, title="The configuration id to be searched for", alias="config_name"
    ),
) -> dict:
    """
    Deactivate a specific configuration UUID

    Keyword Arguments:
        config_id {str} -- [description] UUID of config_id property required

    Returns:
        dict -- [description]
    """
    value = config_update.dict()

    if len(value["configuration_data"]) == 0:
        detail = f"'configuration_data' cannot be empty"
        raise HTTPException(status_code=400, detail=detail)

    if config_id is None and config_name is None:
        detail = f"Either config_id or config_name must be used."
        logger.error(f"Error: {detail}")
        raise HTTPException(status_code=400, detail=detail)
    elif config_id is not None and config_name is not None:
        detail = f"Either config_id or config_name can be used."
        logger.error(f"Error: {detail}")
        raise HTTPException(status_code=400, detail=detail)

    if config_name is not None:
        fetch_query = app_config.select().where(app_config.c.config_name == config_name)
    if config_id is not None:
        fetch_query = app_config.select().where(app_config.c.config_id == config_id)

    db_result = await fetch_one_db(fetch_query)

    rev = db_result["revision"]
    config_information = {
        "config_version": value["config_version"],
        "date_updated": get_current_datetime(),
        "configuration_data": value["configuration_data"],
        "revision": rev + 1,
    }

    # Fetch single row
    if config_name is not None:
        query = app_config.update().where(app_config.c.config_name == config_name)

    if config_id is not None:
        query = app_config.update().where(app_config.c.config_id == config_id)

    values = config_information
    await execute_one_db(query, values)
    db_result = await fetch_one_db(fetch_query)
    c_id = db_result["config_id"]
    c_name = db_result["config_name"]
    logger.info(f"config_id: '{c_id}', config_name: '{c_name}' has been updated")
    return {"config_id": c_id, "config_name": c_name, "status": "updated"}


@router.put(
    "/active-status",
    tags=["configuration"],
    response_description="Deactivated",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def deactivate_config(
    config_id: str = Query(
        None, title="The configuration id to be searched for", alias="config_id"
    ),
    config_name: str = Query(
        None, title="The configuration id to be searched for", alias="config_name"
    ),
    is_active: bool = Query(None, title="by active status", alias="active"),
) -> dict:
    """
    Deactivate a specific config UUID

    Keyword Arguments:
        config_id {str} -- [description] name of config_name property required

    Returns:
        dict -- [description]
    """
    if is_active is None:
        is_active = False

    if config_id is None and config_name is None:
        detail = f"Either config_id or config_name must be used."
        logger.error(f"Error: {detail}")
        raise HTTPException(status_code=400, detail=detail)
    elif config_id is not None and config_name is not None:
        detail = f"Either config_id or config_name can be used."
        logger.error(f"Error: {detail}")
        raise HTTPException(status_code=400, detail=detail)

    # Fetch single row
    config_information = {
        "is_active": is_active,
        "date_updated": get_current_datetime(),
    }
    if config_name is not None:
        query = app_config.update().where(app_config.c.config_name == config_name)
    if config_id is not None:
        query = app_config.update().where(app_config.c.config_id == config_id)

    values = config_information
    await execute_one_db(query, values)

    if config_name is not None:
        fetch_query = app_config.select().where(app_config.c.config_name == config_name)
    if config_id is not None:
        fetch_query = app_config.select().where(app_config.c.config_id == config_id)
    result = await fetch_one_db(fetch_query)
    if result is None:
        # return error if empty results
        detail = f"No results match query criteria"
        logger.error(f"Error: {detail}")
        raise HTTPException(status_code=404, detail=detail)

    update_id = result["config_id"]
    result = {"result": f"config_id {update_id} updated to status of {is_active}"}
    logger.info(result)
    return result


@router.post("/create-config", tags=["configuration"])
async def create_configuration(new_config: AppConfigurationBase) -> dict:

    value = new_config.dict()
    if len(value["configuration_data"]) is 0:
        detail = f"'configuration_data' cannot be empty"
        logger.error(f"Error: 'configuration_data' cannot be empty")
        raise HTTPException(status_code=400, detail=detail)

    config_data = json.dumps(value["configuration_data"])

    create_new_config = {
        "config_id": str(uuid.uuid4()),
        "config_name": value["config_name"],
        "config_version": value["config_version"],
        "date_created": get_current_datetime(),
        "date_updated": get_current_datetime(),
        "is_active": True,
        "configuration_data": value["configuration_data"],
        "revision": 1,
    }
    try:
        query = app_config.insert()
        values = create_new_config
        await execute_one_db(query, values)

        result = {
            "config_id": create_new_config["config_id"],
            "config_name": value["config_name"],
        }
        return result
    except Exception as e:

        if "UNIQUE constraint" in str(e):
            detail = f"config_name must be unique"
            logger.critical(f"Error: {detail}")
            raise HTTPException(status_code=400, detail=detail)
        else:
            logger.error(f"Critical Error: {e}")
            raise HTTPException(status_code=400, detail=str(e))
