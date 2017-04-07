from pycards.cards.card import Card


def test_load_data():
    c = Card('13123123')
    assert c.data is not None


def test_type_data():
    c = Card('13123123')
    assert type(c.data) == dict


def test_empty_data():
    c = Card('13123123')
    assert bool(c.data) is True


def load_load_fixtures():
    assert True is True