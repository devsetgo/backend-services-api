# -*- coding: utf-8 -*-
import uuid
from datetime import datetime
from enum import Enum, IntEnum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator
from sqlalchemy.sql import and_

from core.db_setup import applications
from data_base.common import execute_one_db, fetch_all_db, fetch_one_db

# Shared properties


class ApplicationCreate(BaseModel):
    app_name: str = Field(..., alias="appName", max_length=50)
    description: str = Field(None, alias="description", max_length=500)


class ApplicationStatus(BaseModel):
    id: str
    is_active: bool = False
    name: Optional[str] = None
    description: Optional[str] = None


class ApplicationOut(BaseModel):
    id: str
    app: ApplicationCreate
