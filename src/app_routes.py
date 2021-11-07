# -*- coding: utf-8 -*-
from api import application_routes as applications
from api import audit_routes as audit_log
from api import auth_routes as auth
from api import health_routes as health
from api import logging_routes as log
from api import tools_routes as tools
from api import users_routes as users



def add_routes(app):
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
