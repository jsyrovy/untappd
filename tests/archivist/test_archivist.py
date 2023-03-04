import datetime

import pytest

from archivist import get_beer, get_brewery, get_dt, get_venue, get_id, get_regex_group

TITLE1 = "Jiří S. is drinking a Denali NEIPA by  Bad Flash at U Toulavé pípy"
TITLE2 = "Jiří S. is drinking an Arnoštova Hořká 10 by  Pardubický pivovar at Untappd at Home"


def test_get_dt():
    assert get_dt((2020, 1, 1, 0, 0, 0, 0, 0, 0)) == datetime.datetime(
        2020, 1, 1, 0, 0, 0
    )


def test_get_beer():
    assert get_beer(TITLE1) == "Denali NEIPA"
    assert get_beer(TITLE2) == "Arnoštova Hořká 10"


def test_get_brewery():
    assert get_brewery(TITLE1) == "Bad Flash"
    assert get_brewery(TITLE2) == "Pardubický pivovar"


def test_get_venue():
    assert get_venue(TITLE1) == "U Toulavé pípy"
    assert get_venue(TITLE2) == "Untappd at Home"


def test_get_id():
    assert get_id("https://untappd.com/user/sejrik/checkin/1252442889") == 1252442889


def test_get_regex_group():
    assert get_regex_group(r"select (.*)", "select this") == "this"

    with pytest.raises(ValueError):
        get_regex_group(r"yes", "nope")
