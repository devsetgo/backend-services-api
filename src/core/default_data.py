# -*- coding: utf-8 -*-
"""
Default data for api
"""
import time
import uuid
from datetime import datetime

from fastapi import APIRouter
from loguru import logger

from crud.crud_ops import execute_one_db
from crud.group_crud import check_unique_name

router = APIRouter()

title = "Delay in Seconds"

# add default configuration functions here