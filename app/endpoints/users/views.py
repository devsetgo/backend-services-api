# -*- coding: utf-8 -*-
"""
doc string
"""
import uuid

from fastapi import APIRouter
from fastapi import Form
from fastapi import Path
from fastapi import Query
from loguru import logger

from com_lib.pass_lib import encrypt_pass
from com_lib.pass_lib import verify_pass
from com_lib.simple_functions import get_current_datetime
from db_setup import database
from db_setup import users
from endpoints.users.models import UserCreate  # , UserUpdate,User, UserInDB

router = APIRouter()


@router.get("/list", tags=["users"])
async def user_list(
    qty: int = Query(
        None,
        title="Quanity",
        description="Records to return (max 500)",
        ge=1,
        le=500,
        alias="qty",
    ),
    offset: int = Query(
        None, title="Offset", description="Offset increment", ge=0, alias="offset"
    ),
    is_active: bool = Query(None, title="by active status", alias="active"),
) -> dict:

    """
    list of users

    Keyword Arguments:

        qty {int} -- [description] 100 returned results is default, maximum is 500
        offset {int} -- [description] 0 seconds default
        Active {bool} -- [description] no default as not required, must be Active=true or false if used

    Returns:
        dict -- [description]
    """

    if qty is None:
        qty: int = 100

    if offset is None:
        offset: int = 0

    # Fetch multiple rows
    if is_active is not None:
        query = (
            users.select()
            .where(users.c.is_active == is_active)
            .order_by(users.c.date_created)
            .limit(qty)
            .offset(offset)
        )
        db_result = await database.fetch_all(query)

        count_query = (
            users.select()
            .where(users.c.is_active == is_active)
            .order_by(users.c.date_created)
        )
        total_count = await database.fetch_all(count_query)

    else:

        query = users.select().order_by(users.c.date_created).limit(qty).offset(offset)
        db_result = await database.fetch_all(query)
        count_query = users.select().order_by(users.c.date_created)
        total_count = await database.fetch_all(count_query)

    result_set = []
    for r in db_result:
        # iterate through data and return simplified data set
        user_data = {
            "user_id": r["user_id"],
            "user_name": r["user_name"],
            "first_name": r["first_name"],
            "last_name": r["last_name"],
            "company": r["company"],
            "title": r["title"],
            "is_active": r["is_active"],
        }
        result_set.append(user_data)

    result = {
        "parameters": {
            "returned_results": len(result_set),
            "qty": qty,
            "total_count": len(total_count),
            "offset": offset,
            "filter_active_status": is_active,
        },
        "users": result_set,
    }
    return result


@router.get(
    "/list/count",
    tags=["users"],
    response_description="Get count of users",
    responses={
        404: {"description": "Operation forbidden"},
        500: {"description": "Mommy!"},
    },
)
async def users_list_count(
    is_active: bool = Query(None, title="by active status", alias="active"),
) -> dict:
    """
    Count of users in the database

    Keyword Arguments:

        Active {bool} -- [description] no default as not required, must be Active=true or false if used

    Returns:
        dict -- [description]
    """

    try:
        # Fetch multiple rows
        if is_active is not None:
            query = users.select().where(users.c.is_active == is_active)
            x = await database.fetch_all(query)
        else:
            query = users.select()
            x = await database.fetch_all(query)

        result = {"count": len(x)}
        return result
    except Exception as e:
        logger.error(f"Critical Error: {e}")


@router.get("/{user_id}", tags=["users"], response_description="Get user information")
async def get_user_id(
    user_id: str = Path(..., title="The user id to be searched for", alias="user_id"),
) -> dict:
    """
    User information for requested UUID

    Keyword Arguments:
        user_id {str} -- [description] UUID of user_id property required

    Returns:
        dict -- [description]
    """

    try:
        # Fetch single row
        query = users.select().where(users.c.user_id == user_id)
        db_result = await database.fetch_one(query)

        user_data = {
            "user_id": db_result["user_id"],
            "user_name": db_result["user_name"],
            "first_name": db_result["first_name"],
            "last_name": db_result["last_name"],
            "company": db_result["company"],
            "title": db_result["title"],
            "address": db_result["address"],
            "city": db_result["city"],
            "country": db_result["country"],
            "postal": db_result["postal"],
            "email": db_result["email"],
            "website": db_result["website"],
            "description": db_result["description"],
            "date_created": db_result["date_created"],
            "date_updated": db_result["date_updated"],
            "is_active": db_result["is_active"],
        }
        return user_data

    except Exception as e:
        logger.error(f"Critical Error: {e}")


@router.put(
    "/deactivate/{user_id}",
    tags=["users"],
    response_description="The created item",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def deactivate_user_id(
    *, user_id: str = Path(..., title="The user id to be deactivated", alias="user_id"),
) -> dict:
    """
    Deactivate a specific user UUID

    Keyword Arguments:
        user_id {str} -- [description] UUID of user_id property required

    Returns:
        dict -- [description]
    """
    user_information = {"is_active": False, "date_updated": get_current_datetime()}

    try:
        # Fetch single row
        query = users.update().where(users.c.user_id == user_id)
        values = user_information
        result = await database.execute(query, values)
        return result
    except Exception as e:
        logger.error(f"Critical Error: {e}")


@router.delete(
    "/{user_id}",
    tags=["users"],
    response_description="The deleted item",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def delete_user_id(
    *, user_id: str = Path(..., title="The user id to be deleted", alias="user_id")
) -> dict:
    """
    Delete a user by UUID

    Keyword Arguments:
        user_id {str} -- [description] UUID of user_id property required

    Returns:
        dict -- [result: user UUID deleted]
    """
    try:
        # delete id
        query = users.delete().where(users.c.user_id == user_id)
        await database.execute(query)
        result = {"status": f"{user_id} deleted"}
        return result

    except Exception as e:
        logger.error(f"Critical Error: {e}")


@router.post(
    "/create/",
    tags=["users"],
    response_description="The created item",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def create_user(*, user: UserCreate,) -> dict:
    """
    POST/Create a new User. user_name (unique), firstName, lastName,
    and password are required. All other fields are optional.

    Arguments:
        user {UserCreate} -- [description]

    Keyword Arguments:

    Returns:
        dict -- [user_id: uuid, user_name: user_name]
    """
    value = user.dict()
    hash_pwd = encrypt_pass(value["password"])

    user_information = {
        "user_id": str(uuid.uuid1()),
        "user_name": value["user_name"].lower(),
        "first_name": value["first_name"],
        "last_name": value["last_name"],
        "password": hash_pwd,
        "title": value["title"],
        "company": value["company"],
        "address": value["address"],
        "city": value["city"],
        "country": value["country"],
        "postal": value["postal"],
        "email": value["email"],
        "website": value["website"],
        "description": value["description"],
        "date_created": get_current_datetime(),
        "date_updated": get_current_datetime(),
        "is_active": True,
        "is_superuser": False,
    }

    try:
        query = users.insert()
        values = user_information
        await database.execute(query, values)

        result = {
            "user_id": user_information["user_id"],
            "user_name": value["user_name"],
        }
        return result
    except Exception as e:
        logger.error(f"Critical Error: {e}")


@router.post(
    "/check-pwd/",
    tags=["users"],
    response_description="The created item",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def check_pwd(user_name: str = Form(...), password: str = Form(...)) -> dict:
    """
        Check password function

        Keyword Arguments:
            user_name {str} -- [description] existing user_name required
            password {str} -- [description] password required

        Returns:
            [Dict] -- [result: bool]
    """
    try:
        # Fetch single row
        query = users.select().where(users.c.user_name == user_name.lower())
        db_result = await database.fetch_one(query)
        result = verify_pass(password, db_result["password"])
        print(result)
        logger.info(f"password validation: user: {user_name.lower()} as {result}")
        return {"result": result}

    except Exception as e:
        logger.error(f"Critical Error: {e}")
