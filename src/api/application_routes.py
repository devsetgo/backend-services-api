# -*- coding: utf-8 -*-
"""


"""
from datetime import datetime, date
import uuid

from fastapi import APIRouter, Depends, Form, HTTPException, Path, Query
from loguru import logger

from api.auth_routes import MANAGER
from core.db_setup import applications
from core.simple_functions import get_current_datetime
from data_base.common import execute_one_db, fetch_all_db, fetch_one_db
from models.applications import ApplicationCreate
from sqlalchemy.sql import and_

router = APIRouter()


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
    user_id: str = Query(None, title="User ID", alias="userId"),
    # user=Depends(MANAGER),
) -> dict:

    criteria = []

    if qty is None:
        qty: int = 100

    if offset is None:
        offset: int = 0

    if user_id is not None:
        criteria.append((applications.c.user_id, user_id, "equal"))

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


@router.post("/", tags=["applications"])
async def create_entry(*, entry: ApplicationCreate) -> dict:
    values = entry.dict()
    query = applications.select().where(applications.c.user_id == values["user_id"])
    app_check_result = await fetch_one_db(query)
    values["id"] = uuid.uuid4()
    values["is_active"] = True
    values["date_created"] = get_current_datetime()
    values["date_updated"] = get_current_datetime()
    try:
        app_query = applications.insert()
        app_values = values
        await execute_one_db(query=app_query, values=app_values)
        return app_values
    except Exception as e:
        logger.error(f"Insertion Error: {e}")
