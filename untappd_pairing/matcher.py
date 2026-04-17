from dataclasses import dataclass
from typing import TYPE_CHECKING

from untappd_pairing.normalize import clean_beer_name, clean_brewery_name, normalize_for_compare

if TYPE_CHECKING:
    from untappd_pairing.untappd_search import UntappdCandidate

NAME_OVERLAP_WITH_BREWERY = 0.50
NAME_OVERLAP_WITHOUT_BREWERY = 0.85
BIGRAM_MIN_LEN = 2


@dataclass(frozen=True, kw_only=True)
class MatchResult:
    candidate: UntappdCandidate
    score: float
    brewery_matched: bool = False


def _bigrams(text: str) -> set[str]:
    normalized = normalize_for_compare(text).replace(" ", "")
    if len(normalized) < BIGRAM_MIN_LEN:
        return {normalized} if normalized else set()
    return {normalized[i : i + 2] for i in range(len(normalized) - 1)}


def name_overlap(beer_name: str, candidate_name: str) -> float:
    bigrams_a = _bigrams(clean_beer_name(beer_name))
    bigrams_b = _bigrams(candidate_name)
    if not bigrams_a or not bigrams_b:
        return 0.0
    return len(bigrams_a & bigrams_b) / min(len(bigrams_a), len(bigrams_b))


def brewery_matches(beer_brewery: str, candidate_brewery: str) -> bool:
    beer_tokens = set(normalize_for_compare(clean_brewery_name(beer_brewery)).split())
    candidate_tokens = set(normalize_for_compare(clean_brewery_name(candidate_brewery)).split())
    if not beer_tokens or not candidate_tokens:
        return False
    return beer_tokens.issubset(candidate_tokens)


def _exact_normalized(beer_name: str, candidate_name: str) -> int:
    return int(normalize_for_compare(beer_name) == normalize_for_compare(candidate_name))


def best_match(beer_name: str, beer_brewery: str, candidates: list[UntappdCandidate]) -> MatchResult | None:
    if not candidates:
        return None

    scored = [
        (
            name_overlap(beer_name, c.name),
            _exact_normalized(beer_name, c.name),
            brewery_matches(beer_brewery, c.brewery),
            c,
        )
        for c in candidates
    ]

    def _sort_key(entry: tuple[float, int, bool, UntappdCandidate]) -> tuple[float, int, float]:
        overlap, exact, _matched, candidate = entry
        return (overlap, exact, candidate.rating or 0.0)

    brewery_hits = [t for t in scored if t[2] and t[0] >= NAME_OVERLAP_WITH_BREWERY]
    if brewery_hits:
        brewery_hits.sort(key=_sort_key, reverse=True)
        overlap, _exact, _matched, candidate = brewery_hits[0]
        return MatchResult(candidate=candidate, score=round(overlap, 4), brewery_matched=True)

    strict_hits = [t for t in scored if not t[2] and t[0] >= NAME_OVERLAP_WITHOUT_BREWERY]
    if strict_hits:
        strict_hits.sort(key=_sort_key, reverse=True)
        overlap, _exact, _matched, candidate = strict_hits[0]
        return MatchResult(candidate=candidate, score=round(overlap, 4), brewery_matched=False)

    return None
