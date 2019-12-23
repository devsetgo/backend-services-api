# -*- coding: utf-8 -*-
import random
import uuid

import silly


def user_test_info():
    set_id = str(uuid.uuid1())
    rand_name: str = silly.noun()
    rand_num: int = random.randint(1, 10000)
    username: str = f"{rand_name}-{rand_num}"
    first_name: str = silly.verb()
    last_name: str = rand_name
    password: str = f"{silly.verb()}-{silly.noun()}"
    title: str = silly.title(capitalize=True)
    company: str = silly.company(capitalize=True)
    address: str = silly.address(capitalize=True)
    city: str = silly.city(capitalize=True)
    country: str = silly.country(capitalize=True)
    postal_code: str = silly.postal_code()
    email = silly.email()
    phone = silly.phone_number()
    description: str = silly.paragraph(length=1)
    website = f"https://www.{silly.domain()}"

    result = {
        "user_id": set_id,
        "user_name": username,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
        "title": title,
        "company": company,
        "address": address,
        "city": city,
        "country": country,
        "postal": postal_code,
        "email": email,
        "phone": phone,
        "website": website,
        "description": description,
    }
    return result
