# -*- coding: utf-8 -*-
from loguru import logger
from passlib.hash import bcrypt


def encrypt_pass(pwd: str) -> str:
    hashed_pwd = bcrypt.using(rounds=13).hash(pwd)
    return hashed_pwd


def verify_pass(pwd: str, crypt_pwd: str) -> bool:
    result = bcrypt.verify(pwd, crypt_pwd)
    logger.info(f"password check result is {result}")
    return result
