# -*- coding: utf-8 -*-
import datetime

from cpuinfo import get_cpu_info
from fastapi import APIRouter
from loguru import logger

from health.checks import get_processes

router = APIRouter()

# TODO: detmine method to shutdown/restart python application
# TODO: Determine method to get application uptime


class HealthChecks:
    @router.get("/", tags=["system-health"])
    async def health_main() -> dict:
        """
        GET status, uptime, and current datetime

        Returns:
            dict -- [status: UP, uptime: seconds current_datetime: datetime.now]
        """
        result: dict = {"status": "UP"}
        return result

    @router.get("/system-info", tags=["system-health"])
    async def health_details() -> dict:
        """
        GET Request for CPU and process data

        Returns:
            dict -- [current_datetime: datetime.now, system information: Python and System Information]
        """

        try:
            system_info = get_cpu_info()
            result: dict = {
                "current_datetime": str(datetime.datetime.now()),
                "system_info": system_info,
            }
            logger.info(f"GET system info")
            return result
            # TODO: make more specific Exception
            # BODY: Exception is generic and should be more specific or removed.
        except Exception as e:
            logger.error(f"Error: {e}")

    @router.get("/processes", tags=["system-health"])
    async def health_processes() -> dict:
        """
        GET running processes and filter by python processes

        Returns:
            dict -- [pid, name, username]
        """
        try:
            system_info = get_processes()
            result: dict = {
                "current_datetime": str(datetime.datetime.now()),
                # "note": "this is filter to only return, python, gunicorn,
                # uvicorn, hypercorn, and daphne pids for security",
                "running_processes": system_info,
            }
            logger.info(f"GET processes")
            return result
        except Exception as e:
            logger.error(f"Error: {e}")
