# -*- coding: utf-8 -*-
# import json
# import csv
import unittest

from devsetgo_lib.file_functions import delete_file

# delete_file(filename="test.html", data=html)


class Test(unittest.TestCase):
    def test_clean_up(self):
        files = [
            "test_data_test_user.json",
            "test_data_users.json",
            "test_data_applications.json",
            'test_user_0.json',
            'test_user_1.json',
        ]
        for f in files:
            delete_file(file_name=f)
