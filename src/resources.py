# -*- coding: utf-8 -*-

from loguru import logger

from core.db_setup import create_db, database
from core.logging_config import config_logging
from data_base.users import default_user
from settings import config_settings

async def startup_events():
    """
    Startup events for application
    """
    try:
        # connect to database
        await database.connect()
        logger.info("Connecting to database")

    except Exception as e:
        # log error
        logger.info(f"Error: {e}")
        logger.trace(f"tracing: {e}")

    # initiate log with statement
    if config_settings.release_env.lower() == "dev":
        logger.debug("initiating logging for api")
        logger.info(f"api initiated release_env: {config_settings.release_env}")

    else:
        logger.info(f"api initiated release_env: {config_settings.release_env}")

    # create admin if true
    if config_settings.create_admin == True:
        logger.warning(
            f"Create Admin is {config_settings.create_admin}, system will try to create default admin"
        )
        await default_user()



async def shutdown_events():
    """
    Shut down events
    """
    try:
        # discount database
        await database.disconnect()
        logger.info("Disconnecting from database")
    except Exception as e:
        # log exception
        logger.info("Error: {error}", error=e)
        logger.trace("tracing: {exception} - {e}", error=e)

    logger.info("API shutting down")
