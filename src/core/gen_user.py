# -*- coding: utf-8 -*-
import random
import secrets
import uuid
from datetime import datetime

import silly
from devsetgo_lib.file_functions import save_json


def user_test_info(save: bool = None):
    set_id = str(uuid.uuid1())
    rand_name: str = silly.noun()
    rand_num: int = random.randint(1, 10000)
    username: str = f"{rand_name}{rand_num}"
    email = silly.email()
    notes: str = silly.paragraph(length=1)
    password: str = secrets.token_urlsafe(8)

    result = {
        "id": set_id,
        "userName": username,
        "email": email,
        "password": password,
        "passwordTwo": password,
        "notes": notes,
        "is_active": random.choice([True, False]),
    }
    if save == True:
        save_json(f"test-user-{datetime.now()}.json", result)
    return result
