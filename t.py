# -*- coding: utf-8 -*-
import time

import httpx

from conftest import bearer_session

base_url = "http://localhost:5000/api/v1"


def get_auth():
    t0 = time.time()
    data = {"username": "johndoe", "password": "secret"}
    r = httpx.post(url=f"{base_url}/auth/login", data=data)
    t = r.json()
    t1 = time.time() - t0
    print(f"auth time: {t1:.4f}, token: {t['access_token']}")
    return t["access_token"]


def call_api(access_token):
    headers = {"Authorization": "Bearer " + access_token}
    # print(headers)
    r = httpx.get(url=f"{base_url}/users/list/count", headers=headers)
    return r.status_code


def main():
    t0 = time.time()
    token = get_auth()

    for g in range(1000):

        c = call_api(access_token=token)
        if c != 200:
            print(c)
            t1 = time.time() - t0
            print(f"{t1:.2f}")
            token = get_auth()

        t1 = time.time() - t0
        print(f"{t1:.2f}")
        # time.sleep(0.0002)


if __name__ == "__main__":

    main()
