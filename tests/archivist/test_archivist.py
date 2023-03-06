import datetime

import pytest

from archivist import (
    Record,
    get_beer,
    get_brewery,
    get_dt,
    get_venue,
    get_id,
    get_regex_group,
    get_optional_regex_group,
    is_record_in_db,
    create_record_in_db,
)
from database.auto_init import db

SOURCES = (
    {
        "text": "Jiří S. is drinking a Denali NEIPA by  Bad Flash at U Toulavé pípy",
        "beer": "Denali NEIPA",
        "brewery": "Bad Flash",
        "venue": "U Toulavé pípy",
    },
    {
        "text": "Jiří S. is drinking an Arnoštova Hořká 10 by  Pardubický pivovar at Untappd at Home",
        "beer": "Arnoštova Hořká 10",
        "brewery": "Pardubický pivovar",
        "venue": "Untappd at Home",
    },
    {
        "text": "Jiří S. is drinking a Welzl 16 IPA by  Pivovar Zábřeh",
        "beer": "Welzl 16 IPA",
        "brewery": "Pivovar Zábřeh",
        "venue": None,
    },
)


def test_get_dt():
    assert get_dt((2020, 1, 1, 0, 0, 0, 0, 0, 0)) == datetime.datetime(
        2020, 1, 1, 0, 0, 0
    )


def test_get_beer():
    for source in SOURCES:
        assert get_beer(source["text"]) == source["beer"]


def test_get_brewery():
    for source in SOURCES:
        assert get_brewery(source["text"]) == source["brewery"]


def test_get_venue():
    for source in SOURCES:
        assert get_venue(source["text"]) == source["venue"]


def test_get_id():
    assert get_id("https://untappd.com/user/sejrik/checkin/1252442889") == 1252442889


def test_get_regex_group():
    assert get_regex_group(r"select (.*)", "select this") == "this"

    with pytest.raises(ValueError):
        get_regex_group(r"yes", "nope")


def test_get_optional_regex_group():
    assert get_optional_regex_group(r"select (.*)", "select this") == "this"
    assert get_optional_regex_group(r"yes", "nope") is None


def test_is_record_in_db():
    assert is_record_in_db(Record(1, datetime.datetime.now(), "", "", "", ""))
    assert not is_record_in_db(Record(10, datetime.datetime.now(), "", "", "", ""))


def test_create_record_in_db():
    id_ = 100
    user = "user"
    beer = "pivo"
    brewery = "pivovar"
    venue = "venue"

    create_record_in_db(
        Record(id_, datetime.datetime.now(), user, beer, brewery, venue)
    )

    assert db.query_one(
        "SELECT 1 FROM `archive` WHERE `id` = ? AND `user` = ? AND `beer` = ? AND `brewery` = ? AND `venue` = ?;",
        (id_, user, beer, brewery, venue),
    )
