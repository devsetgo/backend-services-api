# -*- coding: utf-8 -*-
import time
import uuid
from datetime import datetime, timedelta
from random import randint

import silly
from fastapi import BackgroundTasks
from loguru import logger
from starlette.testclient import TestClient
from unsync import unsync

from com_lib.simple_functions import get_current_datetime

# from db_setup import todos
from db_setup import app_config, database, users
from endpoints.sillyusers.gen_user import user_test_info
from settings import NUMBER_CONFIG, NUMBER_USERS

number_of_config = NUMBER_CONFIG
number_of_users = NUMBER_USERS
# time variables
currentTime = datetime.now()


def create_data():

    logger.info(f"creating demo data")
    user_count = count_users().result()
    config_count = count_config().result()

    if int(user_count) == 0:
        create_users(int(number_of_users))
    else:
        logger.info(f"existing data, sample users will not be created")

    if int(config_count) == 0:
        create_config(int(number_of_config))
    else:
        logger.info(f"existing data, sample config will not be created")


@unsync
async def count_users():
    query = users.select()
    count = await database.fetch_all(query)

    result = len(count)
    logger.info(f"number of users in DB: {result}")
    return result


@unsync
async def count_config():
    query = app_config.select()
    count = await database.fetch_all(query)

    result = len(count)
    logger.info(f"number of config in DB: {result}")
    return result


def create_users(create_users: int):

    for _ in range(0, create_users):
        time.sleep(0.01)
        new_user = user_test_info()
        db_user_call(new_user)


def create_config(create_config: int):

    for _ in range(0, create_config):
        time.sleep(0.01)
        config_information = {
            "config_id": str(uuid.uuid4()),
            "config_name": f"{silly.noun()}-{silly.verb()}",
            "config_version": f"{randint(0, 10)}.{randint(0, 99)}",
            "description": silly.sentence(),
            "date_created": get_current_datetime(),
            "date_updated": get_current_datetime(),
            "is_active": True,
            "configuration_data": {
                "installationAt": "Philadelphia, PA",
                "adminEmail": "ksm@pobox.com",
                "poweredBy": "Cofax",
                "poweredByIcon": "/images/cofax.gif",
                "staticPath": "/content/static",
                "templateProcessorClass": "org.cofax.WysiwygTemplate",
                "templateLoaderClass": "org.cofax.FilesTemplateLoader",
                "templatePath": "templates",
                "templateOverridePath": "",
                "defaultListTemplate": "listTemplate.htm",
                "defaultFileTemplate": "articleTemplate.htm",
                "useJSP": False,
                "jspListTemplate": "listTemplate.jsp",
                "jspFileTemplate": "articleTemplate.jsp",
                "cachePackageTagsTrack": randint(0, 1000),
                "cachePackageTagsStore": randint(0, 1000),
                "cachePackageTagsRefresh": randint(0, 1000),
                "cacheTemplatesTrack": randint(0, 1000),
                "cacheTemplatesStore": randint(0, 1000),
                "cacheTemplatesRefresh": randint(0, 1000),
                "cachePagesTrack": randint(0, 1000),
                "cachePagesStore": randint(0, 1000),
                "cachePagesRefresh": randint(0, 1000),
                "cachePagesDirtyRead": randint(0, 1000),
                "dataStoreTestQuery": "SET NOCOUNT ON;select test='test';",
                "dataStoreLogFile": "/usr/local/tomcat/logs/datastore.log",
                "dataStoreInitConns": randint(0, 1000),
                "dataStoreMaxConns": randint(0, 1000),
                "dataStoreConnUsageLimit": randint(0, 1000),
                "dataStoreLogLevel": "debug",
                "maxUrlLength": randint(0, 1000),
            },
        }
        db_config_call(config_information)


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
async def db_config_call(config_information: dict):
    try:
        query = app_config.insert()
        values = config_information
        await database.execute(query, values)
        result = {
            "config_id": config_information["config_id"],
            "config_name": config_information["config_name"],
        }
        logger.info(f"db config call: {result}")
        return result
    except Exception as e:
        logger.critical(f"Create Error: {e}")
