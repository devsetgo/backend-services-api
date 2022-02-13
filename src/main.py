# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from loguru import logger
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from starlette_exporter import PrometheusMiddleware, handle_metrics

import resources
from app_routes import add_routes
from core.custom_middleware import LoggerMiddleware
from core.db_setup import create_db
from core.logging_config import config_logging
from settings import config_settings

# config logging start
config_logging()
logger.info("API Logging initiated")
# database start
create_db()
logger.info("API database initiated")

if config_settings.release_env == "prd":
    debug_value = False
else:
    debug_value = config_settings.debug


# fastapi start
app = FastAPI(
    debug=debug_value,
    title=config_settings.title,
    description=config_settings.description,
    version=config_settings.app_version,
    openapi_url="/openapi.json",
    on_startup=[resources.startup_events],
    on_shutdown=[resources.shutdown_events],
    # openapi_tags=[
    #     "externalDocs": {
    #     "description": "Items external docs",
    #     "url": "https://fastapi.tiangolo.com/",
    # },]
)

logger.info("API App initiated")

# 404
four_zero_four = {404: {"description": "Not found"}}

# add middleware
logger.info("Loading Middleware")
# gzip middelware
app.add_middleware(GZipMiddleware, minimum_size=1000)
# logger middleware
app.add_middleware(LoggerMiddleware)
# session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=config_settings.secret_key,
    max_age=config_settings.max_timeout,
    same_site="strict",
    session_cookie="session_set",
)
# require HTTPS
if config_settings.https_on == True:
    app.add_middleware(HTTPSRedirectMiddleware)
    logger.warning(
        f"https is set to {config_settings.https_on} and will required https connections"
    )

if config_settings.prometheus_on == True:
    app.add_middleware(PrometheusMiddleware)
    logger.info("prometheus middleware enabled")
    app.add_route("/api/health/metrics", handle_metrics)
    logger.info("prometheus route added")


add_routes(app)


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
