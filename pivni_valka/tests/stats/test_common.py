import datetime

from pivni_valka.stats.common import (
    get_total_unique_beers,
    get_unique_beers,
    get_unique_beers_before,
)


def test_get_total_unique_beers():
    assert get_total_unique_beers() == {
        "sejrik": 11,
        "mencik2": 22,
        "Mates511": 33,
        "ominar": 0,
    }


def test_get_unique_beers():
    assert get_unique_beers("sejrik") == "11"
    assert get_unique_beers("sejrik", days=1) == "10"
    assert get_unique_beers("sejrik", days=1, formatted=True) == "+10"
    assert get_unique_beers("ominar") == "0"
    assert get_unique_beers("ominar", formatted=True) == "0"


def test_get_unique_beers_before():
    assert get_unique_beers_before("sejrik", datetime.date.today()) == 11
    assert get_unique_beers_before("sejrik", datetime.date(2022, 1, 2)) == 0
    assert get_unique_beers_before("sejrik", datetime.date(2022, 1, 3)) == 1
