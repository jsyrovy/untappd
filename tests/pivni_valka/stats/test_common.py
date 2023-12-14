import datetime

from sqlalchemy import text

from database.orm import engine
from pivni_valka.stats.common import (
    get_total_unique_beers,
    get_unique_beers,
    get_unique_beers_before,
    save_daily_stats,
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


def test_save_daily_stats():
    def _get_count(_date, _user_name):
        with engine.connect() as conn:
            return conn.execute(
                text(
                    "SELECT SUM(unique_beers) FROM pivni_valka WHERE `date` = :date and user = :user;",
                ).bindparams(date=_date, user=_user_name)
            ).scalar_one()

    date = datetime.date.today()
    user_name = "tester"

    save_daily_stats(date, user_name, 1)
    assert _get_count(date, user_name) == 1

    save_daily_stats(date, user_name, 2)
    assert _get_count(date, user_name) == 2
