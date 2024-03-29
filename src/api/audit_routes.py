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

from fastapi import APIRouter, Query

from core.db_setup import audit_log
from data_base.common import fetch_all_db
from models.audit_log import AuditLogBase

router = APIRouter()


@router.get("/list", tags=["audit log"])
async def audit_log_list(
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
        ..., title="Application ID to get audit log for", alias="appId"
    ),
    date_from: datetime = Query(
        None, title="Date From = farthest back", alias="dateFrom"
    ),
    date_to: datetime = Query(
        None, title="Date to = most current date", alias="dateTo"
    ),
    # user=Depends(MANAGER),
) -> dict:

    criteria = []

    if qty is None:
        qty: int = 100

    if offset is None:
        offset: int = 0

    if app_id is not None:
        criteria.append((audit_log.c.app_id, app_id, "equal"))

    query = (
        audit_log.select().order_by(audit_log.c.date_created).limit(qty).offset(offset)
    )
    count_query = audit_log.select().order_by(audit_log.c.date_created)

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


@router.post("/", tags=["audit log"])
async def create_entry(*, entry: AuditLogBase) -> dict:
    return entry
