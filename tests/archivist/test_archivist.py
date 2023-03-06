import datetime

import pytest

from archivist import (
    get_beer,
    get_brewery,
    get_dt,
    get_venue,
    get_id,
    get_regex_group,
    get_optional_regex_group,
)

TITLE1 = "Jiří S. is drinking a Denali NEIPA by  Bad Flash at U Toulavé pípy"
TITLE2 = "Jiří S. is drinking an Arnoštova Hořká 10 by  Pardubický pivovar at Untappd at Home"
TITLE3 = "Jiří S. is drinking a Welzl 16 IPA by  Pivovar Zábřeh"


def test_get_dt():
    assert get_dt((2020, 1, 1, 0, 0, 0, 0, 0, 0)) == datetime.datetime(
        2020, 1, 1, 0, 0, 0
    )


def test_get_beer():
    assert get_beer(TITLE1) == "Denali NEIPA"
    assert get_beer(TITLE2) == "Arnoštova Hořká 10"
    assert get_beer(TITLE3) == "Welzl 16 IPA"


def test_get_brewery():
    assert get_brewery(TITLE1) == "Bad Flash"
    assert get_brewery(TITLE2) == "Pardubický pivovar"
    assert get_brewery(TITLE3) == "Pivovar Zábřeh"


def test_get_venue():
    assert get_venue(TITLE1) == "U Toulavé pípy"
    assert get_venue(TITLE2) == "Untappd at Home"
    assert get_venue(TITLE3) is None


def test_get_id():
    assert get_id("https://untappd.com/user/sejrik/checkin/1252442889") == 1252442889


def test_get_regex_group():
    assert get_regex_group(r"select (.*)", "select this") == "this"

    with pytest.raises(ValueError):
        get_regex_group(r"yes", "nope")


def test_get_optional_regex_group():
    assert get_optional_regex_group(r"select (.*)", "select this") == "this"
    assert get_optional_regex_group(r"yes", "nope") is None
