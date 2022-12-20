from pivni_valka.stats.common import get_total_unique_beers


def test_get_total_unique_beers():
    assert get_total_unique_beers() == {
        "sejrik": 11,
        "mencik2": 22,
        "Mates511": 33,
        "ominar": 0,
    }
