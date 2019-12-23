# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel
from pydantic import SecretStr


# Shared properties
class AppConfigurationBase(BaseModel):
    config_name: str
    configuration: dict
    config_version: Optional[str] = None
    description: Optional[str] = None


# class ConfigCreate(AppConfigurationBase):
#     user_name: str
#     first_name: str
#     last_name: str
#     password: str
#     title: Optional[str] = None
#     company: Optional[str] = None
#     address: Optional[str] = None
#     city: Optional[str] = None
#     country: Optional[str] = None
#     phone: Optional[str] = None
#     postal: Optional[str] = None
#     email: Optional[str] = None
#     website: Optional[str] = None
#     description: Optional[str] = None
