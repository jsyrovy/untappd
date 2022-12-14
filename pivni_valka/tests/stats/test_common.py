from pivni_valka.stats.common import get_total_unique_beers


def test_get_total_unique_beers():
    assert get_total_unique_beers() == {'Mates511': 43, 'mencik2': 39, 'ominar': 47, 'sejrik': 35}
