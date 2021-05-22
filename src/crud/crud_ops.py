# -*- coding: utf-8 -*-
"""
database simple functions. Pass query and where needed values and get result back
"""


from loguru import logger

from core.db_setup import database


async def fetch_one_db(query):
    try:
        logger.debug(query)
        result = await database.fetch_one(query)
        logger.debug(result)
        return result
    except Exception as e:
        logger.critical(f"error: {e}")
        return e


async def fetch_all_db(query):
    try:
        logger.debug(query)
        result = await database.fetch_all(query)
        logger.debug(result)
        return result
    except Exception as e:
        logger.critical(f"error: {e}")
        return e


async def execute_one_db(query, values: dict = None):

    try:
        logger.debug(query)
        logger.debug(values)
        await database.execute(query, values)
        result = "complete"
        logger.debug(result)
        return result
    except Exception as e:
        logger.critical(f"error: {e}")
        return e
