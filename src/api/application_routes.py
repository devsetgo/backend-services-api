# -*- coding: utf-8 -*-
"""


"""
from datetime import datetime, date
import uuid

from sqlalchemy.sql.expression import false

from fastapi import APIRouter, Depends, Form, HTTPException, Path, Query
from loguru import logger

from api.auth_routes import MANAGER
from core.db_setup import applications, users
from core.simple_functions import get_current_datetime
from data_base.common import execute_one_db, fetch_all_db, fetch_one_db
from models.applications import ApplicationCreate, ApplicationStatus
from sqlalchemy.sql import and_
from collections import OrderedDict

router = APIRouter()


@router.get("/list/admin", tags=["applications"])
async def application_list_admin(
    qty: int = Query(
        None,
        title="Quantity",
        description="Records to return (max 500)",
        ge=1,
        le=500,
        alias="qty",
    ),
    offset: int = Query(
        None, title="Offset", description="Offset increment", ge=0, alias="offset"
    ),
    is_active: bool = Query(
        None,
        title="Active Status",
        description="The status of the application",
        alias="isActive",
    ),
    user_id: str = Query(
        None,
        title="Active Status",
        description="The status of the application",
        alias="userId",
    ),
    user=Depends(MANAGER),
) -> dict:

    if user["is_admin"] == True:

        criteria = []

        if qty is None:
            qty: int = 100

        if offset is None:
            offset: int = 0

        if user_id is not None:
            criteria.append((applications.c.user_id, user_id, "equal"))

        if is_active is not None:
            criteria.append((applications.c.is_active, is_active, "equal"))

        query = (
            applications.select()
            .order_by(applications.c.date_created)
            .limit(qty)
            .offset(offset)
        )
        count_query = applications.select()

        for crit in criteria:
            col, val, logical = crit
            if logical == "greater":
                query = query.where(col == val)
                count_query = count_query.where(col >= val)
            elif logical == "less":
                query = query.where(col == val)
                count_query = count_query.where(col <= val)
            else:
                query = query.where(col == val)
                count_query = count_query.where(col == val)

        db_result = await fetch_all_db(query)
        total_count = await fetch_all_db(count_query)

        result = {
            "parameters": {
                "returned_results": len(db_result),
                "qty": qty,
                "total_count": len(total_count),
                "offset": offset,
            },
            "applications": db_result,
        }
        return result
    else:
        logger.warning(f"{user_id} was not found in database.")
        raise HTTPException(status_code=403, detail="Insuffient Privaliages")


@router.get("/list", tags=["applications"])
async def application_list(
    qty: int = Query(
        None,
        title="Quantity",
        description="Records to return (max 500)",
        ge=1,
        le=500,
        alias="qty",
    ),
    offset: int = Query(
        None, title="Offset", description="Offset increment", ge=0, alias="offset"
    ),
    is_active: bool = Query(
        None,
        title="Active Status",
        description="The status of the application",
        alias="isActive",
    ),
    user=Depends(MANAGER)
    # user=Depends(MANAGER),
) -> dict:

    user_id = user["id"]
    criteria = []

    if qty is None:
        qty: int = 100

    if offset is None:
        offset: int = 0

    if user_id is not None:
        criteria.append((applications.c.user_id, user_id, "equal"))

    if is_active is not None:
        criteria.append((applications.c.is_active, is_active, "equal"))

    query = (
        applications.select()
        .order_by(applications.c.date_created)
        .limit(qty)
        .offset(offset)
    )
    count_query = applications.select()

    for crit in criteria:
        col, val, logical = crit
        if logical == "greater":
            query = query.where(col == val)
            count_query = count_query.where(col >= val)
        elif logical == "less":
            query = query.where(col == val)
            count_query = count_query.where(col <= val)
        else:
            query = query.where(col == val)
            count_query = count_query.where(col == val)

    db_result = await fetch_all_db(query)
    total_count = await fetch_all_db(count_query)

    result = {
        "parameters": {
            "returned_results": len(db_result),
            "qty": qty,
            "total_count": len(total_count),
            "offset": offset,
        },
        "applications": db_result,
    }
    return result


@router.post(
    "/create",
    tags=["applications"],
    status_code=201,
)
async def create_application(
    *, entry: ApplicationCreate, user=Depends(MANAGER)
) -> dict:
    user_id = user["id"]
    values: dict = entry.dict()
    query = users.select().where(users.c.id == user_id)
    app_check_result = await fetch_one_db(query)

    if app_check_result is None:
        logger.warning(f"{user_id} was not found in database.")
        raise HTTPException(status_code=404, detail="User not found")

    id = uuid.uuid4()
    data: dict = {
        "id": id,
        "app_name": values["app_name"],
        "description": values["description"],
        "is_active": True,
        "date_created": get_current_datetime(),
        "date_updated": get_current_datetime(),
    }

    try:
        app_query = applications.insert()
        await execute_one_db(query=app_query, values=data)
        return data
    except Exception as e:
        error: dict = {"database_error": "contact support"}
        logger.error(f"Insertion Error: {e}")
        return error


@router.put("/deactivate", tags=["applications"])
async def deactivate_application(
    *,
    id: str = Query(
        None,
        title="app id",
        description="The ID of the application",
        alias="appId",
    ),
    user=Depends(MANAGER),
) -> dict:

    user_id: str = user["id"]
    if user["is_admin"] == True:
        logger.warning(f"administrator {user_id} is modifying appid {id}")
    else:
        query = applications.select().where(
            and_(applications.c.user_id == user_id, applications.c.id == id)
        )
        user_check_result = await fetch_one_db(query)

        if user_check_result is None:
            logger.warning(f"{user_id} was not found in database.")
            raise HTTPException(status_code=404, detail="User or App ID are incorrect")

    values: dict = {
        "id": id,
        "is_active": False,
        "date_updated": get_current_datetime(),
    }
    try:
        app_query = applications.update().where(applications.c.id == id)
        logger.critical(app_query)
        # app_values = values
        await execute_one_db(query=app_query, values=values)

    except Exception as e:
        error: dict = {"database_error": "contact support"}
        logger.error(f"Insertion Error: {e}")
        return error

    check_result_query = applications.select().where(applications.c.id == values["id"])
    result = await fetch_one_db(query=check_result_query)
    return result


@router.delete("/delete", tags=["applications"])
async def delete_application(
    *,
    id: str = Query(
        None,
        title="app id",
        description="The ID of the application",
        alias="appId",
    ),
    user=Depends(MANAGER),
) -> dict:

    user_id: str = user["id"]
    if user["is_admin"] == True:
        logger.warning(f"administrator {user_id} is modifying appid {id}")
    else:
        query = applications.select().where(
            and_(
                applications.c.user_id == user_id,
                applications.c.id == id,
                applications.c.is_active == False,
            )
        )
        user_check_result = await fetch_one_db(query)

        if user_check_result is None:
            logger.warning(f"{user_id} was not found in database.")
            raise HTTPException(
                status_code=404,
                detail="User or App ID are incorrect or is still active",
            )
    try:
        app_query = applications.delete().where(applications.c.id == id)
        await execute_one_db(query=app_query)

    except Exception as e:
        error: dict = {"database_error": "contact support"}
        logger.error(f"Insertion Error: {e}")
        return error
    check_result_query = applications.select().where(applications.c.id == id)
    result = await fetch_one_db(query=check_result_query)
    if result is None:
        logger.info(f"id {id} deleted from the database by {user_id}")
        return {"status": "deleted"}
    else:
        logger.info(f"id {id} attempted to delete from the database by {user_id}")
        return {"data": result, "error": "the deletion did not work as expected"}
