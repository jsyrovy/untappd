import logging
from dataclasses import dataclass
from urllib.parse import urlencode

from bs4 import BeautifulSoup, Tag

from utils import common

logger = logging.getLogger(__name__)

UNTAPPD_BASE_URL = "https://untappd.com"
SEARCH_TIMEOUT = 10.0


@dataclass(frozen=True, kw_only=True)
class UntappdCandidate:
    name: str
    brewery: str
    url: str
    rating: float | None


def _build_search_url(query: str) -> str:
    qs = urlencode({"q": query, "type": "beer", "sort": "all"})
    return f"{UNTAPPD_BASE_URL}/search?{qs}"


def _parse_rating(beer_item: Tag) -> float | None:
    caps = beer_item.select_one("div.rating div.caps[data-rating]")
    if caps is None:
        return None
    raw = caps.get("data-rating")
    if not raw:
        return None
    raw_str = raw if isinstance(raw, str) else raw[0]
    try:
        rating = float(raw_str)
    except ValueError:
        return None
    return rating if rating > 0 else None


def _parse_beer_item(beer_item: Tag) -> UntappdCandidate | None:
    name_link = beer_item.select_one("p.name a[href^='/b/']")
    brewery_link = beer_item.select_one("p.brewery a")
    if name_link is None or brewery_link is None:
        return None

    href = name_link.get("href")
    if not isinstance(href, str):
        return None

    return UntappdCandidate(
        name=name_link.get_text(strip=True),
        brewery=brewery_link.get_text(strip=True),
        url=f"{UNTAPPD_BASE_URL}{href}",
        rating=_parse_rating(beer_item),
    )


def parse_search_results(html: str) -> list[UntappdCandidate]:
    soup = BeautifulSoup(html, "html.parser")
    results: list[UntappdCandidate] = []
    for beer_item in soup.select("div.results-container div.beer-item"):
        candidate = _parse_beer_item(beer_item)
        if candidate is not None:
            results.append(candidate)
    return results


def search_beer(query: str) -> list[UntappdCandidate]:
    url = _build_search_url(query)
    common.random_sleep(max_=5)
    logger.debug("Untappd search: %s", query)
    html = common.download_page(url, timeout=SEARCH_TIMEOUT)
    return parse_search_results(html)


def parse_beer_page(html: str, url: str) -> UntappdCandidate | None:
    soup = BeautifulSoup(html, "html.parser")
    name_el = soup.select_one("div.name h1")
    brewery_el = soup.select_one("div.name p.brewery a")
    if name_el is None or brewery_el is None:
        return None

    rating: float | None = None
    rating_el = soup.select_one("div.caps[data-rating]")
    if rating_el is not None:
        raw = rating_el.get("data-rating")
        raw_str = raw if isinstance(raw, str) else (raw[0] if raw else "")
        try:
            parsed = float(raw_str)
        except ValueError:
            parsed = 0.0
        rating = parsed if parsed > 0 else None

    return UntappdCandidate(
        name=name_el.get_text(strip=True),
        brewery=brewery_el.get_text(strip=True),
        url=url,
        rating=rating,
    )


def fetch_beer_page(url: str) -> UntappdCandidate | None:
    common.random_sleep(max_=5)
    logger.debug("Untappd beer page: %s", url)
    html = common.download_page(url, timeout=SEARCH_TIMEOUT)
    return parse_beer_page(html, url)
