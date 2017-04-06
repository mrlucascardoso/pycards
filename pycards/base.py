import json
import os
import re

class CreditCard(object):

    _data = None

    def __init__(self, number, expire_month=None, expire_year=None, code=None, cardholder=None):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        with open(os.path.join(BASE_DIR, 'brandcards/data.json')) as data_file:
            data = json.load(data_file)
            if 'brands' in data:
                self._data = dict()
                for item in data['brands']:
                    self._data[item['name']] = item['regex'].replace('\\d', '\d')

        self.number = number
        self.expire_month = expire_month
        self.expire_year = expire_year
        self.code = code
        self.cardholder = cardholder


    @property
    def brand(self):

        return None

