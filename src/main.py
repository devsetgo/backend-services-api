# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from loguru import logger
from starlette.responses import RedirectResponse
from starlette_exporter import PrometheusMiddleware, handle_metrics

from api import auth_routes as auth
from api import health_routes as health
from api import tools_routes as tools
from api import users_routes as users
from api import audit_routes as audit_log
from api import logging_routes as log
from api import application_routes as applications
from core.db_setup import create_db, database
from core.logging_config import config_logging
from data_base.users import default_user
from settings import config_settings
from core.custom_middleware import LoggerMiddleware

# config logging start
config_logging()
logger.info("API Logging initiated")
# database start
create_db()
logger.info("API database initiated")

# fastapi start
app = FastAPI(
    title=config_settings.title,
    description=config_settings.description,
    version=config_settings.app_version,
    openapi_url="/openapi.json",
    # openapi_tags=[
    #     "externalDocs": {
    #     "description": "Items external docs",
    #     "url": "https://fastapi.tiangolo.com/",
    # },]
)

logger.info("API App initiated")
# Add general middelware
# Add prometheus
app.add_middleware(PrometheusMiddleware)
app.add_middleware(LoggerMiddleware)
# Add GZip
app.add_middleware(GZipMiddleware, minimum_size=500)
# 404
four_zero_four = {404: {"description": "Not found"}}
# Endpoint routers
# User router
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["auth"],
    responses=four_zero_four,
)
# User router
app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["users"],
    responses=four_zero_four,
)
# Applications router
app.include_router(
    applications.router,
    prefix="/api/v1/applications",
    tags=["applications"],
    responses=four_zero_four,
)
# Log router
app.include_router(
    log.router,
    prefix="/api/v1/logging",
    tags=["logging"],
    responses=four_zero_four,
)
# Audit Log router
app.include_router(
    audit_log.router,
    prefix="/api/v1/audit-log",
    tags=["audit log"],
    responses=four_zero_four,
)
# Tools router
app.include_router(
    tools.router,
    prefix="/api/v1/tools",
    tags=["tools"],
    responses=four_zero_four,
)
# Health router
app.include_router(
    health.router,
    prefix="/api/health",
    tags=["system-health"],
    responses=four_zero_four,
)


@app.on_event("startup")
async def startup_event():
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

    # require HTTPS
    if config_settings.https_on == True:
        app.add_middleware(HTTPSRedirectMiddleware)
        logger.warning(
            f"https is set to {config_settings.https_on} and will required https connections"
        )

    if config_settings.prometheus_on == True:
        app.add_route("/api/health/metrics", handle_metrics)
        logger.info("prometheus route added")

    if config_settings.create_admin == True:
        logger.warning(
            f"Create Admin is {config_settings.create_admin}, system will try to create default admin"
        )
        await default_user()


@app.on_event("shutdown")
async def shutdown_event():
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


@app.get("/")
async def root():
    """
    Root endpoint of API

    Returns:
        Redrects to openapi document
    """
    # redirect to openapi docs
    response = RedirectResponse(url="/docs")
    return response


@app.get("/info")
async def information():
    """
    API information endpoint

    Returns:
        [json] -- [description] app version, environment running in (dev/prd),
        Doc/Redoc link, Lincense information, and support information
    """
    result = {
        "title": config_settings.title,
        "description": config_settings.description,
        "version": config_settings.app_version,
        "environment": config_settings.release_env,
        "updates": config_settings.updated,
    }
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
