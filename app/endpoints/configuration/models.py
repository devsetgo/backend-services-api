# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, SecretStr


# Shared properties
class AppConfigurationBase(BaseModel):
    config_name: str
    configuration: dict
    config_version: Optional[str] = None
    description: Optional[str] = None


class ConfigUpdate(AppConfigurationBase):
    configuration: dict
    config_version: Optional[str] = None
    description: Optional[str] = None
