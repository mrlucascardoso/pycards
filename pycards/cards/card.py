import re
import json
import math
from datetime import datetime
from pycards.settings import DATABASE_PATH


class NoDatabaseExist(Exception):
    """'File data.json not found.'"""
    pass


class DatabaseBadFormatted(Exception):
    """File data.json in incorrect format."""
    pass


class MultipleMatchesFound(Exception):
    """More than one match for brand regex"""
    pass


class Card(object):
    """
    Base class for credit and debit card
    """

    def __init__(self, number, expire_month=None, expire_year=None, code=None, cardholder=None):
        self._number = str(int(number)).strip()
        self._expire_month = str(int(expire_month)).strip() if expire_month else None
        self._expire_year = str(int(expire_year)).strip() if expire_year else None
        self._expire_year = \
            str(int(math.floor(datetime.now().year/100)))+self._expire_year if expire_year and len(expire_year) == 2 \
            else self._expire_year if expire_year and len(expire_year) == 4 \
            else None
        self._code = str(int(code)).strip() if code else None
        self._cardholder = str(cardholder).strip() if cardholder else None

    @staticmethod
    def _load_data_file():
        try:
            with open(DATABASE_PATH) as data_file:
                return json.load(data_file)
        except FileNotFoundError:
            raise NoDatabaseExist('File data.json in incorrect format.')

    @staticmethod
    def _load_data():
        data = dict()
        json_data = Card._load_data_file()
        if 'brands' in json_data:

            if type(json_data['brands']) is not list:
                raise DatabaseBadFormatted('File data.json in incorrect format. No contains brandcards list')

            if not len(json_data['brands']):
                raise DatabaseBadFormatted('File data.json in incorrect format. No brandcards in list')

            if any(item for item in json_data['brands'] if 'name' not in item or 'regex' not in item):
                raise DatabaseBadFormatted('File data.json in incorrect format. No contains name or regex in items')

            for item in json_data['brands']:
                data[item['name']] = {
                    "regex": item['regex'].replace('\\d', '\d'),
                    "luhn": bool(item['luhn']) if 'luhn' in item else False
                }
        else:
            raise DatabaseBadFormatted('File data.json in incorrect format.')

        return data

    @staticmethod
    def _luhn(number):
        sum = 0
        num_digits = len(number)
        oddeven = num_digits & 1

        for count in range(0, num_digits):

            digit = int(number[count])

            if not ((count & 1) ^ oddeven):
                digit *= 2
            if digit > 9:
                digit -= 9

            sum += digit

        return (sum % 10) == 0

    @property
    def is_valid(self):

        if type(self._number) != str and not len(self._number):
            return False

        brand = self.brand
        if not brand:
            return False

        if self.data[brand]['luhn'] and not Card._luhn(self._number):
            return False  # this card number has an invalid checksum

        if self._expire_month and (int(self._expire_month) < 1 or int(self._expire_month) > 12):

            return False  # this card's expiration month is invalid

        year = datetime.now().year

        if self._expire_year and (int(self._expire_year) < year-20 or int(self._expire_year) > year+20):

            return False  # this card's expiration year is invalid

        if self._code and len(self._code) > 4 or len(self._code) < 3:

            return False  # this card's verification code is the wrong length

        return True

    @property
    def brand(self):
        brand = None

        matches = 0

        for key, value in self.data.items():
            regex = r"{}".format(value['regex'])
            match = re.match(regex, self.number)
            if match:
                brand = key
                matches += 1

        if matches > 1:
            raise MultipleMatchesFound('Multiple matches for brand regex.')

        return brand

    @property
    def data(self):
        return self._load_data()

    @property
    def cardholder(self):
        if not self._cardholder:
            return None

        return self._cardholder

    @property
    def number(self):
        return self._number

    @property
    def expires(self):
        if not self._expire_month or not self._expire_year:
            return None

        return datetime(int(self._expire_year), int(self._expire_month), 1).date()

    @property
    def expires_string(self):
        expires = self.expires
        if not expires:
            return None

        return '{:02d}/{:02d}'.format(expires.month, expires.year - 2000)

    @property
    def is_expired(self):
        expires = self.expires
        if not expires:
            return None

        return datetime.now().date() >= expires

    @property
    def code_name(self):
        return 'CVV'

    @property
    def code(self):
        if not self._code:
            return None

        return self._code
