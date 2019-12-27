# -*- coding: utf-8 -*-
import json
import csv
import unittest

from com_lib.file_functions import delete_file


class Test(unittest.TestCase):
    def test_clean_up(self):
        files = [
            "test_data_test_user.json",
            "test_data_users.json",
        ]
        for f in files:
            delete_file(f)
