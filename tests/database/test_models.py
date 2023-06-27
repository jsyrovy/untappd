import datetime

from database.models import PivniValka


def test_pivni_valka_repr():
    statement = "PivniValka(id=1, date=datetime.datetime(2023, 1, 2, 12, 11, 10, 9), user='user', unique_beers=5)"
    pivni_valka = eval(statement)
    assert pivni_valka.__repr__() == statement
