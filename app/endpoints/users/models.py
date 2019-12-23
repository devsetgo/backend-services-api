# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel
from pydantic import SecretStr


# Shared properties
class UserBase(BaseModel):
    user_name: str
    first_name: str
    last_name: str
    password: str
    title: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None


class UserBaseInDB(UserBase):
    user_id: str = None
    user_name: str


# Properties to receive via API on creation
class UserCreate(UserBase):
    user_name: str
    first_name: str
    last_name: str
    password: str
    title: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    postal: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None


class UserPwd(UserBase):
    user_name: str
    password: SecretStr


# Properties to receive via API on update
class UserDeactivate(UserBaseInDB):
    is_active: bool = False


# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
    first_name: str
    last_name: str
    title: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None


class UserList(UserBaseInDB):
    first_name: str
    last_name: str
    title: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True
