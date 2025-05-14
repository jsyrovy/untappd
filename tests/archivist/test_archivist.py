import datetime
from time import struct_time

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from archivist import (
    create_record_in_db,
    get_beer,
    get_brewery,
    get_dt,
    get_id,
    get_optional_regex_group,
    get_regex_group,
    get_venue,
    is_record_in_db,
)
from database.models import Archive
from database.orm import engine

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
    assert get_dt(struct_time((2020, 1, 1, 0, 0, 0, 0, 0, 0))) == datetime.datetime(2020, 1, 1, 0, 0, 0)


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
    assert is_record_in_db(1)
    assert not is_record_in_db(10)


def test_create_record_in_db():
    id_ = 100
    user = "user"
    beer = "pivo"
    brewery = "pivovar"
    venue = "venue"

    create_record_in_db(
        Archive(
            id=id_,
            dt_utc=datetime.datetime.now(),
            user=user,
            beer=beer,
            brewery=brewery,
            venue=venue,
        ),
    )

    stmt = select(Archive).where(
        Archive.id == id_,
        Archive.user == user,
        Archive.beer == beer,
        Archive.brewery == brewery,
        Archive.venue == venue,
    )
    with Session(engine) as session:
        assert session.execute(stmt).scalar_one()
