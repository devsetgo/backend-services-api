# -*- coding: utf-8 -*-
# import json
# import csv
import datetime
import unittest

from core.simple_functions import get_current_datetime


class Test(unittest.TestCase):
    def test_get_current_datetime(self):
        result = get_current_datetime()
        assert type(result) is datetime.datetime
