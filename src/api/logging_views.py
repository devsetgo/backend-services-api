# -*- coding: utf-8 -*-
import asyncio
import time

from fastapi import APIRouter, Query
from loguru import logger

from core.gen_user import user_test_info

router = APIRouter()

# get log
# post log
# get app

@router.get("/make-one", tags=["silly users"])
async def make_user(
    delay: int = Query(
        None,
        title="silly users",
        description="Seconds (max 121)",
        ge=1,
        le=121,
        alias="delay",
    )
) -> dict:
    """
    GET one random generate user

    Keyword Arguments:
        delay {int} -- [description] delay (sleep) time from 0 to 121 seconds

    Returns:
        dict -- [description] random generation of user data
    """
    t0 = time.time()
    # sleep if delay option is used
    if delay is not None:
        await asyncio.sleep(delay)

    t1: float = time.time() - t0
    response = {
        "delay_time": delay,
        "delay_timer": f"{t1:.8f}",
        "user_info": user_test_info(),
    }
    logger.info(f"process time: {t1:.8f}")
    return response

