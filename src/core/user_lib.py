# -*- coding: utf-8 -*-
from passlib.hash import bcrypt
from passlib.context import CryptContext
from jose import JWTError, jwt


def encrypt_pass(pwd: str) -> str:
    hashed_pwd = bcrypt.using(rounds=13).hash(pwd)
    return hashed_pwd


def verify_pass(pwd: str, crypt_pwd: str) -> bool:
    result = bcrypt.verify(pwd, crypt_pwd)
    return result


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(user_id: str, pd: str):
    pass
