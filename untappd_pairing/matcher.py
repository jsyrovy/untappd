from dataclasses import dataclass
from typing import TYPE_CHECKING

from untappd_pairing.normalize import normalize_for_compare

if TYPE_CHECKING:
    from untappd_pairing.untappd_search import UntappdCandidate

MATCH_THRESHOLD = 0.70
BREWERY_BONUS = 0.15
TIE_BREAKER_DELTA = 0.02
BIGRAM_MIN_LEN = 2


@dataclass(frozen=True, kw_only=True)
class MatchResult:
    candidate: UntappdCandidate
    score: float


def _bigrams(text: str) -> set[str]:
    normalized = normalize_for_compare(text).replace(" ", "")
    if len(normalized) < BIGRAM_MIN_LEN:
        return {normalized} if normalized else set()
    return {normalized[i : i + 2] for i in range(len(normalized) - 1)}


def _jaccard(a: str, b: str) -> float:
    bigrams_a = _bigrams(a)
    bigrams_b = _bigrams(b)
    if not bigrams_a or not bigrams_b:
        return 0.0
    intersection = bigrams_a & bigrams_b
    union = bigrams_a | bigrams_b
    return len(intersection) / len(union)


def _brewery_tokens_subset(beer_brewery: str, candidate_brewery: str) -> bool:
    beer_tokens = set(normalize_for_compare(beer_brewery).split())
    candidate_tokens = set(normalize_for_compare(candidate_brewery).split())
    if not beer_tokens or not candidate_tokens:
        return False
    return beer_tokens.issubset(candidate_tokens)


def score_candidate(beer_name: str, beer_brewery: str, candidate: UntappdCandidate) -> float:
    base = _jaccard(beer_name, candidate.name)
    if _brewery_tokens_subset(beer_brewery, candidate.brewery):
        base += BREWERY_BONUS
    return min(base, 1.0)


def best_match(beer_name: str, beer_brewery: str, candidates: list[UntappdCandidate]) -> MatchResult | None:
    if not candidates:
        return None

    scored = [(score_candidate(beer_name, beer_brewery, c), c) for c in candidates]
    scored.sort(key=lambda pair: (pair[0], pair[1].rating or 0.0), reverse=True)

    top_score, top_candidate = scored[0]
    if top_score < MATCH_THRESHOLD:
        return None

    if len(scored) > 1:
        second_score, second_candidate = scored[1]
        if top_score - second_score < TIE_BREAKER_DELTA and (second_candidate.rating or 0.0) > (
            top_candidate.rating or 0.0
        ):
            top_candidate = second_candidate
            top_score = second_score

    return MatchResult(candidate=top_candidate, score=round(top_score, 4))
