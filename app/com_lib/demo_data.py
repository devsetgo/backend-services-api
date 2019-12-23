# -*- coding: utf-8 -*-
import random
import uuid
from datetime import datetime, timedelta

from fastapi import BackgroundTasks
import silly
from loguru import logger
from starlette.testclient import TestClient

from db_setup import database

# from db_setup import todos
from db_setup import users
from endpoints.sillyusers.gen_user import user_test_info
from unsync import unsync

NUMBER_TASKS = 10
NUMBER_USERS = 10
# time variables
currentTime = datetime.now()


def create_data():

    logger.info(f"creating demo data")
    user_count = count_users().result()
    task_count = count_tasks().result()

    if int(user_count) == 0:
        create_users(int(NUMBER_USERS))
    else:
        logger.info(f"existing data, sample users will not be created")

    if int(task_count) == 0:
        create_tasks(int(NUMBER_TASKS))
    else:
        logger.info(f"existing data, sample tasks will not be created")


@unsync
async def count_users():
    query = users.select()
    count = await database.fetch_all(query)

    result = len(count)
    logger.info(f"number of users in DB: {result}")
    return result


@unsync
async def count_tasks():
    query = todos.select()
    count = await database.fetch_all(query)

    result = len(count)
    logger.info(f"number of tasks in DB: {result}")
    return result


def create_users(create_users: int):

    for _ in range(0, create_users):
        new_user = user_test_info()
        db_user_call(new_user)
        user_id = new_user["user_id"]


def create_tasks(create_tasks: int):

    for _ in range(0, create_tasks):
        todo_information = {
            "todo_id": str(uuid.uuid1()),
            "title": silly.thing(),
            "description": silly.sentence(),
            "date_due": currentTime + timedelta(days=random.randint(1, 180)),
            "is_complete": bool(random.getrandbits(1)),
            "date_create": currentTime,
            "date_update": currentTime,
            "user_id": str(uuid.uuid4()),
            # ,'checklist': []
            "date_complete": None,
        }

        db_todo_call(todo_information)


@unsync
async def db_user_call(new_user: dict):
    try:
        query = users.insert()
        values = new_user
        await database.execute(query, values)

        result = {
            "user_id": new_user["user_id"],
            # "user_name": new_user["user_name"],
        }
        logger.info(f"db user call: {result}")
        return result
    except Exception as e:
        logger.error(f"Critical Error: {e}")


@unsync
async def db_todo_call(todo_information: dict):
    try:
        query = todos.insert()
        values = todo_information
        db_call = await database.execute(query, values)
        result = {"todo_id": todo_information["todo_id"]}
        logger.info(f"db todo call: {result}")
        return result
    except Exception as e:
        logger.critical(f"Create Error: {e}")
