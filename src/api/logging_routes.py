# -*- coding: utf-8 -*-
"""
User routes to perform actions
list users
list user count
user create
user profile
user update profile
user password verify
user update password
user delete
user deactivate
user unlock

"""
from datetime import datetime
import uuid

from fastapi import APIRouter, Depends, Form, HTTPException, Path, Query
from loguru import logger

from api.auth_routes import MANAGER
from core.db_setup import logging_info, users, applications
from core.simple_functions import get_current_datetime
from data_base.common import execute_one_db, fetch_all_db, fetch_one_db
from models.logging_models import LoggingBase
from data_base.users import get_user_details
from sqlalchemy import desc
from sqlalchemy.sql import and_

router = APIRouter()


@router.get("/list", tags=["logging"])
async def logging_list(
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
    app_id: str = Query(
        None, title="Application ID to get audit log for", alias="appId"
    ),
    # date_from: datetime = Query(
    #     None, title="Date From = farthest back", alias="dateFrom"
    # ),
    # date_to: datetime = Query(
    #     None, title="Date to = most current date", alias="dateTo"
    # ),
    # user=Depends(MANAGER),
) -> dict:

    criteria = []

    if qty is None:
        qty: int = 100

    if offset is None:
        offset: int = 0

    if app_id is not None:
        criteria.append((logging_info.c.app_id, app_id, "equal"))

    query = (
        logging_info.select()
        .order_by(desc(logging_info.c.record_date))
        .limit(qty)
        .offset(offset)
    )
    count_query = logging_info.select().order_by(logging_info.c.date_created)

    for crit in criteria:
        col, val, logical = crit
        if logical == "greater":
            query = query.where(col == val)
            count_query = count_query.where(col <= val)
        elif logical == "less":
            query = query.where(col == val)
            count_query = count_query.where(col >= val)
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
        "audit_log": db_result,
    }
    return result


# log count
# log ID


@router.post("/", tags=["logging"])
async def create_log_entry(*, entry: LoggingBase, user=Depends(MANAGER)) -> dict:

    user_id = user["id"]
    values: dict = entry.dict()

    query = applications.select().where(
        and_(applications.c.user_id == user_id, applications.c.id == id)
    )
    app_check_result = await fetch_one_db(query)

    if app_check_result is None:
        logger.warning(f"{user_id} was not found in database.")
        raise HTTPException(status_code=404, detail="User not found")

    log_id = str(uuid.uuid4())
    values["id"] = log_id
    values["date_created"] = get_current_datetime()

    try:
        app_query = logging_info.insert()
        app_values = values
        db_status = await execute_one_db(query=app_query, values=app_values)
        result: dict = {"id": log_id, "status": db_status}
        return result
    except Exception as e:
        #
        error: dict = {"database_error": "contact support", "error": e}
        logger.error(f"Insertion Error: {error}")
        return error
