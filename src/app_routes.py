# -*- coding: utf-8 -*-
from api import application_routes as applications
from api import audit_routes as audit_log
from api import auth_routes as auth
from api import health_routes as health
from api import logging_routes as log
from api import tools_routes as tools
from api import users_routes as users


router_responses: dict = {
    302: {"description": "The item was moved"},
    400: {"description": "Bad request"},
    401: {"description": "Unauthorized"},
    403: {"description": "Insufficient privileges"},
    404: {"description": "Not found"},
    418: {
        "I_am-a_teapot": "The server refuses the attempt to \
                brew coffee with a teapot."
    },
    429: {"description": "Rate limit exceeded"},
}


def add_routes(app):
    # HTTP Responses
    router_responses: dict = {
        302: {"description": "The item was moved"},
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Insufficient privileges"},
        404: {"description": "Not found"},
        418: {
            "I_am-a_teapot": "The server refuses the attempt to \
                brew coffee with a teapot."
        },
        429: {"description": "Rate limit exceeded"},
    }
    # Endpoint routers
    # User router
    app.include_router(
        auth.router,
        prefix="/api/v1/auth",
        tags=["auth"],
        responses=router_responses,
    )
    # User router
    app.include_router(
        users.router,
        prefix="/api/v1/users",
        tags=["users"],
        responses=router_responses,
    )
    # Applications router
    app.include_router(
        applications.router,
        prefix="/api/v1/applications",
        tags=["applications"],
        responses=router_responses,
    )
    # Log router
    app.include_router(
        log.router,
        prefix="/api/v1/logging",
        tags=["logging"],
        responses=router_responses,
    )
    # Audit Log router
    app.include_router(
        audit_log.router,
        prefix="/api/v1/audit-log",
        tags=["audit log"],
        responses=router_responses,
    )
    # Tools router
    app.include_router(
        tools.router,
        prefix="/api/v1/tools",
        tags=["tools"],
        responses=router_responses,
    )
    # Health router
    app.include_router(
        health.router,
        prefix="/api/health",
        tags=["system-health"],
        responses=router_responses,
    )
