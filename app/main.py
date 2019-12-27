# -*- coding: utf-8 -*-
import pyjokes
import uvicorn
from fastapi import FastAPI, Query
from loguru import logger
from starlette.responses import RedirectResponse

from com_lib.demo_data import create_data
from com_lib.logging_config import config_logging
from db_setup import create_db, database
from endpoints.configuration import views as config_app
from endpoints.sillyusers import views as silly_users
from endpoints.tools import views as tools
from endpoints.users import views as users
from health import views as health
from settings import (
    APP_VERSION,
    CREATE_SAMPLE_DATA,
    HOST_DOMAIN,
    LICENSE_LINK,
    LICENSE_TYPE,
    OWNER,
    RELEASE_ENV,
    WEBSITE,
)

# config logging start
config_logging()
logger.info("API Logging initiated")
# database start
create_db()
logger.info("API database initiated")
# fastapi start
app = FastAPI(
    title="Backend Services API",
    description="API for user and configuration",
    version=APP_VERSION,
    openapi_url="/openapi.json",
)
logger.info("API App initiated")

four_zero_four = {404: {"description": "Not found"}}
# Endpoint routers
# Configuration router
app.include_router(
    config_app.router,
    prefix="/api/v1/configuration",
    tags=["configuration"],
    responses=four_zero_four,
)
# User router
app.include_router(
    users.router, prefix="/api/v1/users", tags=["users"], responses=four_zero_four,
)
# Converter router
app.include_router(
    tools.router, prefix="/api/v1/tools", tags=["tools"], responses=four_zero_four,
)

# Silly router
app.include_router(
    silly_users.router,
    prefix="/api/v1/silly-users",
    tags=["silly users"],
    responses=four_zero_four,
)

# Health router
app.include_router(
    health.router,
    prefix="/api/health",
    tags=["system-health"],
    responses=four_zero_four,
)

"""
for future use
app.include_router(socket.router,prefix="/api/v1/websocket",
tags=["websocket"],responses=four_zero_four,)
"""

# startup events
@app.on_event("startup")
async def startup_event():

    try:
        await database.connect()
        logger.info(f"Connecting to database")

    except Exception as e:
        logger.info(f"Error: {e}")
        logger.trace(f"tracing: {e}")

    # initiate log with statement
    if RELEASE_ENV.lower() == "dev":
        logger.debug(f"Initiating logging for API")
        logger.info(f"API initiated Release_ENV: {RELEASE_ENV}")

        if CREATE_SAMPLE_DATA == "True":
            create_data()

    else:
        logger.info(f"API initiated Release_ENV: {RELEASE_ENV}")


@app.on_event("shutdown")
async def shutdown_event():

    try:
        await database.disconnect()
        logger.info("Disconnecting from database")
    except Exception as e:
        logger.info("Error: {error}", error=e)
        logger.trace("tracing: {exception} - {e}", error=e)

    logger.info("API shutting down")


@app.get("/")
async def index():
    """
    Root endpoint of API

    Returns:
        Redrects to openapi document
    """
    response = RedirectResponse(url="/docs")
    return response


@app.get("/information")
async def info():
    """
    API information endpoint

    Returns:
        [json] -- [description] app version, environment running in (dev/prd),
        Doc/Redoc link, Lincense information, and support information
    """
    if RELEASE_ENV.lower() == "dev":
        main_url = "http://localhost:5000"
    else:
        main_url = HOST_DOMAIN

    openapi_url = f"{main_url}/docs"
    redoc_url = f"{main_url}/redoc"
    result = {
        "App Version": APP_VERSION,
        "Environment": RELEASE_ENV,
        "Docs": {"OpenAPI": openapi_url, "ReDoc": redoc_url},
        "License": {"Type": LICENSE_TYPE, "License Link": LICENSE_LINK},
        "Application_Information": {"Owner": OWNER, "Support Site": WEBSITE},
    }
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
