# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum, IntEnum


# Shared properties
class LoggingBase(BaseModel):
    app_id: str = Field(..., alias="appId", max_length=50)
    reference_id: str = Field(..., alias="referenceId", max_length=50)
    record_date: datetime = Field(
        None,
        alias="recordDate",
        example=datetime.now() - timedelta(seconds=7),
    )
    record_str: str = Field(
        None,
        alias="recordStr",
        min_length=5,
        max_length=500,
        example="Bob did something",
    )
    record_json: dict = Field(
        None,
        alias="recordJson",
        example={"data": "is free form", "user": "Bob", "thing": "did something"},
    )

    @validator("record_str")
    def record_str_blank(cls, v, values, **kwargs):
        if "record_str" == None and values["record_dict"] == None:
            raise ValueError("Either record_str or record_dict must have data.")
        return v

    @validator("record_json")
    def record_json_blank(cls, v, values, **kwargs):
        if "record_json" == None and values["record_str"] == None:
            raise ValueError("Either recordStr or recordDict must have data.")
        return v
