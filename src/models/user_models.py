# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, Field


# Shared properties
class UserBase(BaseModel):
    user_name: str
    email: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True


class UserBaseInDB(UserBase):
    # user_id: str = None
    user_name: str


# Properties to receive via API on creation
class UserCreate(UserBase):
    user_name: str
    email: Optional[str] = None
    notes: Optional[str] = None
    password: str


class UserPwd(UserBase):
    user_name: str
    password: str


# Properties to receive via API on update
class UserDeactivate(UserBaseInDB):
    is_active: bool = False


# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
    user_name: str
    email: Optional[str] = None
    notes: Optional[str] = None


class UserList(UserBaseInDB):
    user_name: str
    email: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True


class UserDeactiveModel(BaseModel):
    id: str
    is_active: bool = Field(
        False,
        alias="isActive",
        title="Status of user",
        example="false",
    )
