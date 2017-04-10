import json
import pytest
from pycards import CreditCard
from datetime import datetime
from pycards.settings import FIXTURES_PATH


@pytest.fixture(scope="session")
def data():
    with open(FIXTURES_PATH) as data_file:
        return json.load(data_file)['AMEX']


def test_init(data):
    assert len(data) > 0
    cards = [CreditCard(card['name'], code=card['code']) for card in data]
    assert len(cards) == len(data)


def test_is_valid(data):
    assert all(CreditCard(card['name'], code=card['code']).is_valid for card in data)


def test_brand(data):
    cards = [CreditCard(card['name'], code=card['code']) for card in data]
    assert len(cards) == len([card for card in cards if card.brand == 'Amex'])


def test_cardholder(data):
    cards = [CreditCard(card['name'], code=card['code'], cardholder='TESTE DADOS') for card in data]
    assert len(cards) == len([card for card in cards if card.cardholder == 'TESTE DADOS'])


def test_number(data):
    numbers = [card['name'] for card in data]
    cards = [CreditCard(card['name'], code=card['code']) for card in data]
    assert all([True for c in cards if c.number in numbers]) and any([True for c in cards if c.number in numbers])


def test_expires(data):
    cards = [CreditCard(card['name'], code=card['code'], expire_month='7', expire_year='2021') for card in data]
    assert all(True for c in cards if type(c.expires) == datetime)


def test_expires_string(data):
    cards = [CreditCard(card['name'], code=card['code'], expire_month='7', expire_year='2021') for card in data]
    assert all(True for c in cards if c.expires_string == '07/21') and any(True for c in cards if c.expires_string == '07/21')


def test_is_not_expired(data):
    card = [CreditCard(card['name'], code=card['code'], expire_month='7', expire_year='2021') for card in data][0]
    assert not card.is_expired


def test_is_expired(data):
    card = [CreditCard(card['name'], code=card['code'], expire_month='7', expire_year='2016') for card in data][0]
    assert card.is_expired


def test_code_name(data):
    card = [CreditCard(card['name'], code=card['code'], expire_month='7', expire_year='2016') for card in data][0]
    assert card.code_name == 'CVV'


def test_code(data):
    codes = [card['code'] for card in data]
    cards = [CreditCard(card['name'], code=card['code']) for card in data]
    assert all([True for c in cards if c.code in codes]) and any([True for c in cards if c.code in codes])
