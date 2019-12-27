# -*- coding: utf-8 -*-


from db_setup import database


async def fetch_one_db(query):

    result = await database.fetch_one(query)
    return result


async def fetch_all_db(query):

    result = await database.fetch_all(query)
    return result


async def execute_one_db(query, values: dict):

    result = await database.execute(query, values)
    return result
