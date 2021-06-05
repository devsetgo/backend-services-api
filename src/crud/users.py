from core.db_setup import users
from core.simple_functions import get_current_datetime
from crud.common import execute_one_db,fetch_all_db
from core.user_lib import encrypt_pass
from settings import config_settings
from loguru import logger
import uuid

async def default_user():

    in_db_query = users.select()
    in_db_result = await fetch_all_db(in_db_query)
    print(in_db_result)
    if len(in_db_result) == 0:

        hash_pwd = encrypt_pass(config_settings.password)
        values = {
            "id": str(uuid.uuid1()),
            "user_name": config_settings.admin_user_name,
            "email": config_settings.admin_email,
            "notes": "created by default setup",
            "password": hash_pwd,
            "date_create": get_current_datetime(),
            "date_updated": get_current_datetime(),
            "last_login": None,
            "is_active": True,
            "is_superuser": True,
            "is_approved":True,
            }
        query = users.insert()
        await execute_one_db(query=query, values=values)
        logger.warning(f"database is empty and default user {config_settings.admin_user_name} has been created")        
    else:
        logger.warning(f"database is not empty and default user {config_settings.admin_user_name} has not been created")

async def last_login(user_name: str):
    last_login = get_current_datetime()
    values: dict = {"last_login": last_login}
    query = query = users.update().where(users.c.user_name == user_name)
    await execute_one_db(query=query, values=values)
    logger.info(f"updating last login for {user_name}")
    
