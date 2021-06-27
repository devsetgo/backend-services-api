# -*- coding: utf-8 -*-
import datetime
import uuid
from datetime import timedelta, datetime
import random
from loguru import logger
from sqlalchemy.sql.functions import user

from core.db_setup import users, applications
from core.simple_functions import get_current_datetime
from core.user_lib import encrypt_pass
from data_base.common import execute_one_db, fetch_all_db, fetch_one_db
from settings import config_settings


async def default_user():

    in_db_query = users.select()
    in_db_result = await fetch_all_db(in_db_query)
    logger.debug(in_db_result)
    if len(in_db_result) == 0:
        logger.info(f"there are 0 users in database, creating default admin")
        hash_pwd = encrypt_pass(config_settings.admin_password)
        user_id: str = str(uuid.uuid1())
        values = {
            "id": user_id,
            "user_name": config_settings.admin_user_name,
            "email": config_settings.admin_email,
            "notes": "created by default setup",
            "password": hash_pwd,
            "date_created": get_current_datetime(),
            "date_updated": get_current_datetime(),
            "last_login": None,
            "is_active": True,
            "is_admin": True,
            "is_approved": True,
        }
        query = users.insert()
        await execute_one_db(query=query, values=values)
        logger.warning(
            f"database is empty and default user {config_settings.admin_user_name} has been created"
        )
        count = 1
        for i in range(30):
            name: str = f"test app {count}"
            app_values = {
                "id": str(uuid.uuid4()),
                "name": name,
                "description": "a test app",
                "user_id": user_id,
                "is_active": True,
                "date_created": get_current_datetime()
                - timedelta(days=random.randint(70, 700)),
                "date_updated": get_current_datetime(),
            }
            app_query = applications.insert()
            await execute_one_db(query=app_query, values=app_values)
            logger.info(f"creating test app {name}")
            count += 1
        logger.warning(
            f"database is empty and default user {config_settings.admin_user_name} has been created"
        )

    else:
        logger.warning(
            f"database is not empty and default user {config_settings.admin_user_name} has not been created"
        )


async def last_login(user_name: str):
    last_login = get_current_datetime()
    values: dict = {"last_login": last_login}
    query = query = users.update().where(users.c.user_name == user_name)
    await execute_one_db(query=query, values=values)
    logger.info(f"updating last login for {user_name}")


# user details
async def get_user_details(user_id: str):
    """
    User details minus hashed password
    """
    try:
        query = users.select().where(users.c.id == user_id)
        data = await fetch_one_db(query)
        result = dict(data)
        result.pop(password)
        return result
    except Exception as e:
        error: dict = {"error": e}
        logger.critical(f"error: {error}")
        return error
