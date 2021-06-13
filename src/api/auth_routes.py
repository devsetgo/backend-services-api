# -*- coding: utf-8 -*-
import secrets
import uuid
from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from loguru import logger

from core.db_setup import users
from core.user_lib import verify_pass
from data_base.common import execute_one_db, fetch_one_db
from data_base.users import last_login
from models.users import RegisterOut, UserCreate

SECRET: str = secrets.token_urlsafe(64)

router = APIRouter()

MANAGER = LoginManager(SECRET, "/api/v1/auth/login", use_cookie=True, use_header=True)


@MANAGER.user_loader
async def get_user_from_db(username: str):
    """
    Retrieve a user from the Database
    :param str username: The username of the user, used as a unique key in the database
    :return dict: The responding user
    """
    query = users.select().where(users.c.user_name == username.lower())
    db_result = await fetch_one_db(query)

    data: dict = dict(db_result)
    logger.debug(data)
    return data


@router.post("/register", status_code=201, response_model=RegisterOut)
async def register(
    create_user: UserCreate,
):
    create_user: dict = create_user.dict()
    create_user["id"] = uuid.uuid4()
    create_user["is_approved"] = False

    query = users.insert()
    db_result = await execute_one_db(query=query, values=create_user)

    return create_user


# remember this should be the same URL we used when initializing the LoginManager
@router.post("/login", status_code=200)
async def login(data: OAuth2PasswordRequestForm = Depends()):
    # here we can use OAuth2PasswordRequestForm provided by FastAPI, so we dont have
    # to define the Dependency ourselves. More at the FastAPI docs
    # https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#oauth2passwordrequestform
    username = data.username
    password = data.password

    logger.debug(f"username: {username}, password: {password}")
    # now lets check if the user is in our db and if the password matches
    # user = get_user_from_db(username)
    query = users.select().where(users.c.user_name == username.lower())
    db_result = await fetch_one_db(query)
    logger.debug(db_result)
    if db_result is None:
        logger.warning(f"username {username} does not exist in database")
        raise InvalidCredentialsException
    else:
        result = verify_pass(password, db_result["password"])
        logger.info(f"user: {username} password check is {result}")
        if result == False:
            logger.warning(f"password is not a matche for username {username}")
            raise InvalidCredentialsException

    await last_login(user_name=username)
    # now we create a token which our user can (for a specific time) use to access protected routes
    access_token = MANAGER.create_access_token(
        # data is the value of the token
        # sub should be the key used to look up the user in the database later on
        # in our case thats the username, as `get_user_from_db` needs the username as a parameter
        data={
            "sub": username,
            "is_admin": db_result["is_admin"],
        },
        expires=timedelta(hours=1),
    )

    # now we can return the encrypted token
    return {"access_token": access_token}


@router.get("/me")
async def logged_in_users_only(user=Depends(MANAGER)):
    # if the request is now made from a client which has logged in and a valid access_token
    # is either in the header or as a cookie, if cookie authorization has been
    # set on initialization of the manager, in the Request fastapi-login will automatically
    # provide the user object from our database to this function.
    # for example if the 'admin' user has logged in and has the token in the headers
    # `user` would equal {'username': 'admin', 'password': 'hashed-password'}, the same as
    # `get_user_from_db`
    pop_list: list = ["password"]
    for i in pop_list:
        user.pop(i)
    return {"user": user}
