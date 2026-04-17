from untappd_pairing.matcher import MATCH_THRESHOLD, best_match, score_candidate
from untappd_pairing.untappd_search import UntappdCandidate


def _candidate(name, brewery="Wild Creatures", url="https://untappd.com/b/x/1", rating=4.0):
    return UntappdCandidate(name=name, brewery=brewery, url=url, rating=rating)


def test_score_high_for_exact_name_and_brewery():
    candidate = _candidate("Tears of St Laurent (2020)")
    score = score_candidate("Tears of St Laurent (2020)", "Wild Creatures", candidate)
    assert score >= 0.95


def test_score_brewery_bonus_applies_when_subset():
    base = score_candidate("Hazy IPA", "Falkon", _candidate("Hazy Pale Ale", brewery="Other"))
    boosted = score_candidate("Hazy IPA", "Falkon", _candidate("Hazy Pale Ale", brewery="Pivovar Falkon"))
    assert boosted > base
    assert boosted - base >= 0.10


def test_score_no_bonus_when_brewery_missing():
    score = score_candidate("IPA", "", _candidate("IPA", brewery="Anything"))
    assert score < MATCH_THRESHOLD + 0.5


def test_best_match_returns_none_below_threshold():
    candidates = [_candidate("Pilsner Urquell", brewery="Plzeňský Prazdroj")]
    assert best_match("Tears of St Laurent (2020)", "Wild Creatures", candidates) is None


def test_best_match_returns_top_score():
    candidates = [
        _candidate("Other Beer", brewery="Other Brewery", rating=4.5),
        _candidate("Tears of St Laurent (2020)", brewery="Wild Creatures", rating=4.0),
    ]
    result = best_match("Tears of St Laurent (2020)", "Wild Creatures", candidates)
    assert result is not None
    assert result.candidate.name == "Tears of St Laurent (2020)"


def test_best_match_tie_breaker_prefers_higher_rating():
    high_rated = _candidate("Tears of St Laurent (2020)", rating=4.5, url="https://untappd.com/b/high/1")
    low_rated = _candidate("Tears of St Laurent (2020)", rating=3.5, url="https://untappd.com/b/low/2")
    result = best_match("Tears of St Laurent (2020)", "Wild Creatures", [low_rated, high_rated])
    assert result is not None
    assert result.candidate.url == "https://untappd.com/b/high/1"


def test_best_match_handles_no_candidates():
    assert best_match("IPA", "Brewery", []) is None
