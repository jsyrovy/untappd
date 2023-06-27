import datetime

from database.models import PivniValka, Archive


def test_pivni_valka_repr():
    pivni_valka = PivniValka(
        id=1,
        date=datetime.datetime(2023, 1, 2, 12, 11, 10, 9),
        user="user",
        unique_beers=5,
    )
    assert (
        repr(pivni_valka)
        == "PivniValka(id=1, date=datetime.datetime(2023, 1, 2, 12, 11, 10, 9), user='user', unique_beers=5)"  # noqa: E501 # pylint: disable=line-too-long
    )


def test_archive_repr():
    archive = Archive(
        id=1,
        dt_utc=datetime.datetime(2023, 1, 2, 12, 11, 10, 9),
        user="user",
        beer="beer",
        brewery="brewery",
        venue="venue",
    )
    assert (
        repr(archive)
        == "Archive(id=1, dt_utc=datetime.datetime(2023, 1, 2, 12, 11, 10, 9), user='user', beer='beer', brewery='brewery', venue='venue')"  # noqa: E501 # pylint: disable=line-too-long
    )
