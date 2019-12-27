0# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, SecretStr, Field


# Shared properties
class AppConfigurationBase(BaseModel):
    config_name: str = Field(..., title="configuration name", max_length=100)
    configuration: dict  = Field(..., title="configuration data")
    config_version: str = Field(None, title="configuration name", max_length=20)
    description: str = Field(None, title="configuration name", max_length=2000)


class ConfigUpdate(BaseModel):
    configuration: dict  = Field(..., title="configuration data")
    config_version: str = Field(None, title="configuration name", max_length=20)
    description: str = Field(None, title="configuration name", max_length=2000)
