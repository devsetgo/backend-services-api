# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from loguru import logger
from starlette.responses import RedirectResponse
from starlette_exporter import PrometheusMiddleware, handle_metrics

from api import health_routes as health
from api import tool_routes as tools
from api import user_routes as users
from core.db_setup import create_db, database
from core.logging_config import config_logging
from settings import config_settings, Settings

# config logging start
config_logging()
logger.info("API Logging initiated")
# database start
create_db()
logger.info("API database initiated")
# fastapi start
app = FastAPI(
    title="Test API",
    description="Checklist APIs",
    version=config_settings.app_version,
    openapi_url="/openapi.json",
)
logger.info("API App initiated")
# Add general middelware
# Add prometheus
app.add_middleware(PrometheusMiddleware)
# Add GZip
app.add_middleware(GZipMiddleware, minimum_size=500)
# 404
four_zero_four = {404: {"description": "Not found"}}
# Endpoint routers
# User router
app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["users"],
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
        "app version": config_settings.app_version,
        "environment": config_settings.release_env,
    }
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")