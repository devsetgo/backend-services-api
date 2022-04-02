# -*- coding: utf-8 -*-
import multiprocessing
import platform
import sys

import psutil
from loguru import logger

# TODO: Make a status that gets app uptime
# BODY: how to get uptime of app, not running os.
# Such as dockerimage or how long the code has been running.


def get_platform() -> dict:
    """
    [summary]
    Get all system, OS, and Python version information

    Returns:
        dict -- ["os": os,
        "system": system,
        "node": node,
        "processor": processor,
        "cpu_count": cpu_count,
        "memory_use": memory_use,
        "python_version": python_version,]
    """
    os = platform.platform()
    processor = platform.processor()
    node = platform.node()
    system = platform.system()
    cpu_count = multiprocessing.cpu_count()
    memory_use = sys.getsizeof({})
    friendly_maxsize = {2 ** 31 - 1: "32 bit", 2 ** 63 - 1: "64 bit"}.get(
        sys.maxsize
    ) or "unknown bits"
    friendly_version = f"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}\
         {sys.version_info[3]}"
    python_version = "{0} ({1})".format(friendly_version, friendly_maxsize)

    result = {
        "os": os,
        "system": system,
        "node": node,
        "processor": processor,
        "cpu_count": cpu_count,
        "memory_use": memory_use,
        "python_version": python_version,
    }
    return result


def get_processes() -> list:
    """
    Get running processes and filter by python processes

    Returns:
        dict -- [pid, name, username]
    """
    result = []
    proc = psutil.process_iter(attrs=["pid", "name", "username"])
    process_check = ["python", "python3", "gunicorn", "uvicorn", "hypercorn", "daphne"]

    for p in proc:
        if p.info["name"] in process_check:
            result.append(p.info)

    logger.debug(result)
    return result
