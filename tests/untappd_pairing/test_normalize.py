from untappd_pairing.normalize import (
    build_search_queries,
    clean_beer_name,
    clean_brewery_name,
    normalize_for_compare,
    strip_diacritics,
)


def test_clean_beer_name_strips_degree():
    assert clean_beer_name("Zappa 12°") == "Zappa"
    assert clean_beer_name("Sumeček 11° IPA") == "Sumeček IPA"


def test_clean_beer_name_strips_parentheses():
    assert clean_beer_name("Tears of St Laurent (2020)") == "Tears of St Laurent"
    assert clean_beer_name("BA Stout (Bourbon Cask)") == "BA Stout"


def test_clean_beer_name_strips_batch_suffix():
    assert clean_beer_name("DIPA Batch #4") == "DIPA"
    assert clean_beer_name("Sour Vol. 2") == "Sour"
    assert clean_beer_name("Hazy IPA série 12") == "Hazy IPA"


def test_clean_beer_name_collapses_whitespace():
    assert clean_beer_name("  Foo   Bar  ") == "Foo Bar"


def test_clean_brewery_name_strips_pivovar():
    assert clean_brewery_name("Pivovar Matuška") == "Matuška"
    assert clean_brewery_name("pivovar Falkon") == "Falkon"
    assert clean_brewery_name("Wild Creatures") == "Wild Creatures"


def test_strip_diacritics():
    assert strip_diacritics("Plzeňský Prazdroj") == "Plzensky Prazdroj"
    assert strip_diacritics("Černý potok") == "Cerny potok"


def test_normalize_for_compare_lowercases_and_strips_diacritics():
    assert normalize_for_compare("Plzeňský  Prazdroj") == "plzensky prazdroj"


def test_build_search_queries_orders_specific_first():
    queries = build_search_queries("Tears of St Laurent (2020)", "Wild Creatures")
    assert queries[0] == "Tears of St Laurent (2020) Wild Creatures"
    assert "Tears of St Laurent Wild Creatures" in queries
    assert queries[-1] == "Tears of St Laurent"


def test_build_search_queries_dedupes():
    queries = build_search_queries("IPA", "")
    assert queries == ["IPA"]


def test_build_search_queries_drops_empty():
    queries = build_search_queries("12°", "")
    assert queries == ["12°"]
