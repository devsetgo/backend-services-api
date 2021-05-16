# -*- coding: utf-8 -*-
import logging
from pathlib import Path

from loguru import logger


from settings import config_settings


def config_logging():
    # remove default logger
    logger.remove()
    # set file path
    cwd = Path.cwd()
    p = cwd.parent
    log_path = p.joinpath("logging").joinpath("log.log")
    # log_path = p.joinpath("logfile").joinpath("log.log")
    # add new configuration
    logger.add(
        log_path,  # log file path
        level=config_settings.loguru_logging_level.upper(),  # logging level
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",  # format of log
        enqueue=True,  # set to true for async or multiprocessing logging
        backtrace=False,  # turn to false if in production to prevent data leaking
        rotation=config_settings.loguru_rotation,  # file size to rotate
        retention=config_settings.loguru_retention,  # how long a the logging data persists
        compression="zip",  # log rotation compression
        serialize=False,  # if you want it json style, set to true. but also change the format
    )

    # intercept standard logging
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    logging.basicConfig(
        handlers=[InterceptHandler()],
        level=config_settings.loguru_logging_level.upper(),
    )