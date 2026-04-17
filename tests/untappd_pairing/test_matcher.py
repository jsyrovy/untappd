from untappd_pairing import matcher
from untappd_pairing.untappd_search import UntappdCandidate


def _candidate(name, brewery="Wild Creatures", url="https://untappd.com/b/x/1", rating=4.0):
    return UntappdCandidate(name=name, brewery=brewery, url=url, rating=rating)


def test_name_overlap_full_for_exact_match():
    assert matcher.name_overlap("Tears of St Laurent", "Tears of St Laurent") == 1.0


def test_name_overlap_full_when_short_name_contained_in_long_name():
    assert matcher.name_overlap("JUNO", "Juno 11° Czech Ale") == 1.0
    assert matcher.name_overlap("Velikonoční", "Velikonoční Ležák 12 a Půl") == 1.0


def test_name_overlap_strips_parenthetical_aliases_from_beer_name():
    # tap-api sometimes appends an alias in parens that's not in the Untappd canonical name
    assert matcher.name_overlap("PP (Pořádné Pivo)", "PP 12%") == 1.0


def test_name_overlap_handles_diacritics_and_punctuation():
    assert matcher.name_overlap("Maisels Weisse", "Maisel's Weisse Original") >= 0.85


def test_name_overlap_low_for_different_beers():
    assert matcher.name_overlap("Pilsner", "Stout") < 0.3


def test_brewery_matches_subset_with_pivovar_prefix():
    assert matcher.brewery_matches("Loutkář", "Pivovar Loutkař") is True


def test_brewery_matches_subset_with_brewery_suffix():
    assert matcher.brewery_matches("Haksna", "Haksna Brewery") is True


def test_brewery_matches_strips_city_suffix_before_comparison():
    assert matcher.brewery_matches("JungBerg, Hořice", "Pivovar JungBerg") is True
    assert matcher.brewery_matches("Maisel, Bayreuth, Bavorsko", "Brauerei Gebr. Maisel") is True


def test_brewery_matches_returns_false_when_disjoint():
    assert matcher.brewery_matches("Loutkář", "Copper Bottom Brewing") is False


def test_brewery_matches_returns_false_when_either_is_empty():
    assert matcher.brewery_matches("", "Pivovar Loutkař") is False
    assert matcher.brewery_matches("Loutkář", "") is False


def test_best_match_prefers_brewery_match_over_higher_name_score():
    copper_bottom = _candidate("Juno", brewery="Copper Bottom Brewing", url="https://untappd.com/b/cb/1")
    loutkar = _candidate("Juno 11° Czech Ale", brewery="Pivovar Loutkař", url="https://untappd.com/b/loutkar/2")
    result = matcher.best_match("JUNO", "Loutkař", [copper_bottom, loutkar])
    assert result is not None
    assert result.candidate.url == "https://untappd.com/b/loutkar/2"
    assert result.brewery_matched is True


def test_best_match_falls_back_to_strict_when_no_brewery_match():
    candidate = _candidate("Tears of St Laurent (2020)", brewery="Wild Creatures Brewery")
    result = matcher.best_match("Tears of St Laurent (2020)", "Unknown Brewery Name", [candidate])
    assert result is not None
    assert result.brewery_matched is False


def test_best_match_returns_none_when_no_brewery_and_loose_name():
    candidate = _candidate("Pilsner Urquell", brewery="Plzeňský Prazdroj")
    result = matcher.best_match("Tears of St Laurent (2020)", "Wild Creatures", [candidate])
    assert result is None


def test_best_match_returns_none_when_brewery_matches_but_name_unrelated():
    candidate = _candidate("Pilsner", brewery="Pivovar Loutkař")
    result = matcher.best_match("Stout", "Loutkař", [candidate])
    assert result is None


def test_best_match_tie_breaker_prefers_higher_rating_within_brewery_tier():
    high = _candidate("Juno", brewery="Pivovar Loutkař", url="https://untappd.com/b/h/1", rating=4.5)
    low = _candidate("Juno", brewery="Pivovar Loutkař", url="https://untappd.com/b/l/2", rating=3.5)
    result = matcher.best_match("Juno", "Loutkař", [low, high])
    assert result is not None
    assert result.candidate.url == "https://untappd.com/b/h/1"


def test_best_match_prefers_exact_normalized_match_over_other_vintage():
    # Same brewery, both names contain the cleaned form, but only one is the exact 2020 vintage
    older = _candidate("Tears of St Laurent (2019)", brewery="Wild Creatures", url="https://untappd.com/b/2019/1")
    matching = _candidate("Tears of St Laurent (2020)", brewery="Wild Creatures", url="https://untappd.com/b/2020/2")
    result = matcher.best_match("Tears of St Laurent (2020)", "Wild Creatures, Mikulov", [older, matching])
    assert result is not None
    assert result.candidate.url == "https://untappd.com/b/2020/2"


def test_best_match_handles_no_candidates():
    assert matcher.best_match("IPA", "Brewery", []) is None


def test_best_match_brewery_path_loose_threshold_accepts_partial_name_overlap():
    candidate = _candidate("Hazy Pale Ale", brewery="Pivovar Falkon")
    result = matcher.best_match("Hazy IPA", "Falkon", [candidate])
    assert result is not None
    assert result.brewery_matched is True


def test_best_match_strict_path_rejects_same_partial_overlap_without_brewery():
    candidate = _candidate("Hazy Pale Ale", brewery="Other Brewery")
    result = matcher.best_match("Hazy IPA", "Falkon", [candidate])
    assert result is None
