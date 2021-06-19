# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum, IntEnum
from core.db_setup import applications
from data_base.common import execute_one_db, fetch_all_db, fetch_one_db
from sqlalchemy.sql import and_

# Shared properties


class ApplicationCreate(BaseModel):
    app_name: str = Field(..., alias="appName", max_length=50)
    description: str = Field(None, alias="description", max_length=500)
    

class ApplicationStatus(BaseModel):
    app_id: str = Field(..., alias="appId", max_length=50)
    is_active:bool = False
    app_name: str = Field(None, alias="appName", max_length=50)
    description: str = Field(None, alias="description", max_length=500)
