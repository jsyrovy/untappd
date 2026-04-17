import logging

import httpx

from robot.base import BaseRobot
from untappd_pairing import matcher, normalize, tap_api, untappd_search
from untappd_pairing import overrides as overrides_module
from untappd_pairing.matcher import MatchResult
from untappd_pairing.store import PAIRINGS_PATH, PairingsStore, beer_key

logger = logging.getLogger(__name__)

UNMATCHED_NO_CANDIDATES = "no_candidates_above_threshold"
UNMATCHED_UPSTREAM_ERROR = "upstream_error"
UNMATCHED_OVERRIDE_PARSE_FAILED = "override_page_parse_failed"
OVERRIDE_QUERY_MARKER = "<override>"


class UntappdPairing(BaseRobot):
    def _main(self) -> None:
        store = PairingsStore.load(PAIRINGS_PATH)
        overrides = overrides_module.load(overrides_module.OVERRIDES_PATH)

        if self._args.local:
            logger.info("Local mode: skipping tap-api fetch and Untappd scraping")
            store.save(PAIRINGS_PATH)
            return

        beers = tap_api.fetch_all_beers()
        logger.info("Fetched %d beers from tap-api", len(beers))

        pending = store.select_pending(beers, overrides=overrides)
        logger.info("Pairing %d pending beers (rest already paired or in cooldown)", len(pending))

        for beer in pending:
            self._pair_one(beer, store, overrides)

        store.save(PAIRINGS_PATH)
        logger.info("Saved %s (pairings=%d, unmatched=%d)", PAIRINGS_PATH, len(store.pairings), len(store.unmatched))

    @staticmethod
    def _pair_one(beer: tap_api.TapBeer, store: PairingsStore, overrides: dict[str, str]) -> None:
        key = beer_key(beer.source, beer.brewery, beer.name)
        if key in overrides:
            UntappdPairing._pair_via_override(beer, store, overrides[key])
            return

        UntappdPairing._pair_via_search(beer, store)

    @staticmethod
    def _pair_via_override(beer: tap_api.TapBeer, store: PairingsStore, url: str) -> None:
        try:
            candidate = untappd_search.fetch_beer_page(url)
        except httpx.HTTPError:
            logger.exception("Failed to fetch override URL %s", url)
            store.record_unmatched(beer, UNMATCHED_UPSTREAM_ERROR)
            return

        if candidate is None:
            logger.error("Could not parse override beer page %s", url)
            store.record_unmatched(beer, UNMATCHED_OVERRIDE_PARSE_FAILED)
            return

        result = MatchResult(candidate=candidate, score=1.0, brewery_matched=True)
        logger.info("Override matched %s::%s -> %s", beer.brewery, beer.name, url)
        store.record_match(beer, result, OVERRIDE_QUERY_MARKER)

    @staticmethod
    def _pair_via_search(beer: tap_api.TapBeer, store: PairingsStore) -> None:
        queries = normalize.build_search_queries(beer.name, beer.brewery)

        for query in queries:
            try:
                candidates = untappd_search.search_beer(query)
            except httpx.HTTPError:
                logger.exception("Untappd search failed for '%s'", query)
                store.record_unmatched(beer, UNMATCHED_UPSTREAM_ERROR)
                return

            result = matcher.best_match(beer.name, beer.brewery, candidates)
            if result is not None:
                logger.info(
                    "Matched %s::%s -> %s (score=%.2f)",
                    beer.brewery,
                    beer.name,
                    result.candidate.url,
                    result.score,
                )
                store.record_match(beer, result, query)
                return

        logger.info("No match for %s::%s after %d queries", beer.brewery, beer.name, len(queries))
        store.record_unmatched(beer, UNMATCHED_NO_CANDIDATES)
