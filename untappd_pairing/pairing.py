import logging

import httpx

from robot.base import BaseRobot
from untappd_pairing import matcher, normalize, tap_api, untappd_search
from untappd_pairing.store import PAIRINGS_PATH, PairingsStore

logger = logging.getLogger(__name__)

UNMATCHED_NO_CANDIDATES = "no_candidates_above_threshold"
UNMATCHED_UPSTREAM_ERROR = "upstream_error"


class UntappdPairing(BaseRobot):
    def _main(self) -> None:
        store = PairingsStore.load(PAIRINGS_PATH)

        if self._args.local:
            logger.info("Local mode: skipping tap-api fetch and Untappd scraping")
            store.save(PAIRINGS_PATH)
            return

        beers = tap_api.fetch_all_beers()
        logger.info("Fetched %d beers from tap-api", len(beers))

        pending = store.select_pending(beers)
        logger.info("Pairing %d pending beers (rest already paired or in cooldown)", len(pending))

        for beer in pending:
            self._pair_one(beer, store)

        store.save(PAIRINGS_PATH)
        logger.info("Saved %s (pairings=%d, unmatched=%d)", PAIRINGS_PATH, len(store.pairings), len(store.unmatched))

    @staticmethod
    def _pair_one(beer: tap_api.TapBeer, store: PairingsStore) -> None:
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
