# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, Field


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
