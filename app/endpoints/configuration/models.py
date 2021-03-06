# -*- coding: utf-8 -*-
0  # -*- coding: utf-8 -*-

from pydantic import BaseModel
from pydantic import Field


# Shared properties
class AppConfigurationBase(BaseModel):
    config_name: str = Field(..., title="configuration name", max_length=100)
    configuration_data: dict = Field(..., title="configuration data")
    config_version: str = Field(None, title="configuration name", max_length=20)
    description: str = Field(None, title="configuration name", max_length=2000)


class ConfigUpdate(BaseModel):
    configuration_data: dict = Field(..., title="configuration data")
    config_version: str = Field(None, title="configuration name", max_length=20)
    description: str = Field(None, title="configuration name", max_length=2000)
