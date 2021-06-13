# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


# Shared properties
class UserBase(BaseModel):
    user_name: str = Field(..., alias="userName")
    email: EmailStr = Field(..., alias="email")
    notes: Optional[str] = None
    is_active: bool = True


class UserBaseInDB(BaseModel):
    # user_id: str = None
    id: str = Field(..., alias="id")
    user_name: str = Field(..., alias="userName")
    email: EmailStr = Field(..., alias="email")
    notes: str = Field(..., alias="notes")
    date_created: datetime = Field(..., alias="created")
    date_updated: datetime = Field(..., alias="updated")
    is_active: bool = Field(..., alias="isActive")
    is_admin: bool = Field(..., alias="isAdmin")
    is_approved: bool = Field(..., alias="isApproved")


class UserAdmin(BaseModel):
    id: str = Field(..., alias="id")
    is_admin: bool = Field(..., alias="isAdmin")


# Properties to receive via API on creation
class UserCreate(BaseModel):
    user_name: str = Field(..., alias="userName")
    email: EmailStr = Field(..., alias="email")
    password: str = Field(..., alias="password")
    password_two: str = Field(..., alias="passwordTwo")
    notes: Optional[str] = None

    @validator("email")
    def email_reject(cls, v):
        bad_domains: list = ["example.com", "example.net", "example.org"]
        for b in bad_domains:
            if b in v:
                raise ValueError("Fake domains are not allowed")
        return v

    @validator("password_two")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v

    @validator("user_name")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v


class RegisterOut(BaseModel):
    id: str
    user_name: str
    email: EmailStr
    is_approved: bool = False


class UserPwd(UserBase):
    user_name: str = Field(..., alias="userName")
    password: str


# Properties to receive via API on update
class UserDeactivate(UserBaseInDB):
    is_active: bool = False


# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
    user_name: str = Field(..., alias="userName")
    email: Optional[EmailStr] = None
    notes: Optional[str] = None


class UserList(UserBaseInDB):
    user_name: str = Field(..., alias="userName")
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
