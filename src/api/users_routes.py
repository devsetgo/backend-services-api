# -*- coding: utf-8 -*-
"""
TODO: Cleanup and add user api endpoints
User routes to perform actions
list users
list user count
user create
user profile
user update profile
user password verify
user update password
user delete
user deactivate
user unlock

"""
import uuid

from fastapi import APIRouter, Depends, Form, HTTPException, Path, Query
from loguru import logger

from api.auth_routes import MANAGER
from core.db_setup import users
from core.simple_functions import get_current_datetime
from core.user_lib import encrypt_pass, verify_pass
from data_base.common import execute_one_db, fetch_all_db, fetch_one_db
from models.users import UserAdmin, UserCreate, UserDeactiveModel

router = APIRouter()


@router.get("/list", tags=["users"])
async def user_list(
    qty: int = Query(
        None,
        title="Quantity",
        description="Records to return (max 500)",
        ge=1,
        le=500,
        alias="qty",
    ),
    offset: int = Query(
        None, title="Offset", description="Offset increment", ge=0, alias="offset"
    ),
    is_active: bool = Query(None, title="by active status", alias="active"),
    user_name: str = Query(None, title="User name", alias="username"),
    email: str = Query(None, title="Email", alias="email"),
    user=Depends(MANAGER),
) -> dict:

    """
    list of users

    Keyword Arguments:
        qty {int} -- [description] 100 returned results is default,
        maximum is 500
        offset {int} -- [description] 0 seconds default
        Active {bool} -- [description] no default as not required,
        must be Active=true or false if used

    Returns:
        dict -- [description]

    """
    criteria = []

    if qty is None:
        qty: int = 100

    if offset is None:
        offset: int = 0

    if user_name is not None:
        criteria.append((users.c.user_name, user_name))

    if email is not None:
        criteria.append((users.c.email, email))

    if is_active is not None:
        criteria.append((users.c.is_active, is_active))

    query = users.select().order_by(users.c.date_created).limit(qty).offset(offset)
    count_query = users.select().order_by(users.c.date_created)

    for crit in criteria:
        col, val = crit
        query = query.where(col == val)
        count_query = count_query.where(col == val)

    db_result = await fetch_all_db(query)
    total_count = await fetch_all_db(count_query)

    result_set = []
    for r in db_result:
        # iterate through data and return simplified data set
        user_data = {
            "id": r["id"],
            "user_name": r["user_name"],
            "email": r["email"],
            "is_active": r["is_active"],
        }
        result_set.append(user_data)

    result = {
        "parameters": {
            "returned_results": len(result_set),
            "qty": qty,
            "total_count": len(total_count),
            "offset": offset,
            "filter": is_active,
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
    user=Depends(MANAGER),
) -> dict:
    """
    Count of users in the database

    Keyword Arguments:
        Active {bool} -- [description] no default as not required,
        must be Active=true or false if used

    Returns:
        dict -- [description]
    """

    try:
        # Fetch multiple rows
        if is_active is not None:
            query = users.select().where(users.c.is_active == is_active)
            data = await fetch_all_db(query)
        else:
            query = users.select()
            data = await fetch_all_db(query)

        result = {"count": len(data)}
        return result
    except Exception as e:
        logger.error(f"Critical Error: {e}")


@router.get("/{userId}", tags=["users"], response_description="Get user information")
async def get_user_id(
    user_id: str = Path(..., title="The user id to be searched for", alias="userId"),
    user=Depends(MANAGER),
) -> dict:
    """
    User information for requested UUID

    Keyword Arguments:
        user_id {str} -- [description] UUID of id property required

    Returns:
        dict -- [description]
    """
    # Fetch single row
    query = users.select().where(users.c.id == user_id)
    db_result = await fetch_one_db(query)

    if db_result is None:
        logger.warning(f"Error: ID {user_id} not found")
        raise HTTPException(status_code=404, detail="ID not found")
    else:
        user_data = {
            "id": db_result["id"],
            "user_name": db_result["user_name"],
            "email": db_result["email"],
            "notes": db_result["notes"],
            "date_created": db_result["date_created"],
            "date_updated": db_result["date_updated"],
            "is_active": db_result["is_active"],
        }
        return user_data


@router.post(
    "/create",
    tags=["users"],
    response_description="The created item",
    status_code=201,
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def create_user(
    *,
    user_create: UserCreate,
    user=Depends(MANAGER),
) -> dict:
    """
    POST/Create a new User. user_name (unique), firstName, lastName,
    and password are required. All other fields are optional.

    Arguments:
        user {UserCreate} -- [description]

    Keyword Arguments:

    Returns:
        dict -- [user_id: uuid, user_name: user_name]
    """
    value = user_create.dict()
    hash_pwd = encrypt_pass(value["password"])

    user_information = {
        "id": str(uuid.uuid1()),
        "user_name": value["user_name"].lower(),
        "email": value["email"],
        "notes": value["notes"],
        "password": hash_pwd,
        "date_created": get_current_datetime(),
        "date_updated": get_current_datetime(),
        "is_active": True,
        "is_admin": False,
    }

    try:
        query = users.insert()
        values = user_information
        await execute_one_db(query, values)

        result = {
            "id": user_information["id"],
            "user_name": value["user_name"],
            "is_active": True,
        }
        return result
    except Exception as e:
        logger.error(f"Insertion Error: {e}")


@router.post(
    "/check-pwd",
    tags=["users"],
    response_description="The created item",
    status_code=201,
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def check_pwd(
    user_name: str = Form(...),
    password: str = Form(...),
    user=Depends(MANAGER),
) -> dict:
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
        db_result = await fetch_one_db(query)
        logger.critical(f"user retrieve erro: {db_result}")
        result = verify_pass(password, db_result["password"])
        logger.info(f"password validation: user: {user_name.lower()} as {result}")
        return {"result": result}

    except Exception as e:
        logger.error(f"Critical Error: Password Validation Error: {e}")


@router.put(
    "/status",
    tags=["users"],
    response_description="The created item",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def set_status_user_id(
    *,
    user_data: UserDeactiveModel,
    user=Depends(MANAGER),
) -> dict:
    """
    Set status of a specific user UUID

    Args:
        user_data (UserDeactiveModel): [id = UUID of user, isActive = True or False]

    Returns:
        dict: [description]
    """
    """
    Set status of a specific user UUID

    Keyword Arguments:
        user_id {str} -- [description] UUID of user_id property required

    Returns:
        dict -- [description]
    """

    values = user_data.dict()
    values["date_updated"] = get_current_datetime()

    try:
        # Fetch single row
        query = users.update().where(users.c.user_id == values["user_id"])
        await execute_one_db(query=query, values=values)
        result: dict = values
        return result
    except Exception as e:
        logger.error(f"Critical Error: {e}")


@router.put(
    "/admin",
    tags=["users"],
    response_description="Setting admin ",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def set_admin_user_id(
    *,
    user_data: UserAdmin,
    user=Depends(MANAGER),
) -> dict:

    if user["is_admin"] == True:

        values = user_data.dict()
        user_id = values["id"]
        values["date_updated"] = get_current_datetime()
        check_user_query = users.select().where(users.c.id == user_id)
        check_user_result = await fetch_one_db(query=check_user_query)

        if check_user_result is None:
            logger.warning(f"{user_id} was not found in database.")
            raise HTTPException(status_code=404, detail="User not found")

        try:
            # Fetch single row
            query = users.update().where(users.c.user_id == user_id)
            await execute_one_db(query=query, values=values)
            result = values
            return result
        except Exception as e:
            logger.error(f"Query_Error: {e}")
    else:
        logger.warning(
            f"user {user['id']} not authorized to access endpoint. Request rejected."
        )
        raise HTTPException(
            status_code=401,
            detail="User not authorized to make request and data logged for attempted request.",
        )


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
    *,
    user_id: str = Path(..., title="The user id to be deleted", alias="user_id"),
    user=Depends(MANAGER),
) -> dict:
    """
    Delete a user by UUID

    Keyword Arguments:
        user_id {str} -- [description] UUID of user_id property required

    Returns:
        dict -- [result: user UUID deleted]
    """
    check_query = users.select().where(users.c.id == user_id)
    db_result = await fetch_one_db(check_query)

    if db_result is None:
        logger.warning(f"Error: ID {user_id} not found")
        raise HTTPException(status_code=404, detail="ID not found")

    try:
        # delete id
        query = users.delete().where(users.c.user_id == user_id)
        await execute_one_db(query)
        result = {"status": f"{user_id} deleted"}
        return result

    except Exception as e:
        logger.error(f"Critical Error: {e}")
