from pathlib import Path
from unittest import mock

from untappd_pairing import untappd_search

FIXTURES = Path(__file__).parent / "fixtures"


def _read_fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_parse_search_results_extracts_candidates():
    html = _read_fixture("untappd_search_tears.html")
    candidates = untappd_search.parse_search_results(html)

    assert candidates, "expected at least one candidate"
    first = candidates[0]
    assert first.name == "Tears of St Laurent (2020)"
    assert first.brewery == "Wild Creatures"
    assert first.url == "https://untappd.com/b/wild-creatures-tears-of-st-laurent-2020/5776418"
    assert first.rating == 4.02


def test_parse_search_results_empty_page():
    html = _read_fixture("untappd_search_empty.html")
    assert untappd_search.parse_search_results(html) == []


def test_parse_handles_missing_rating():
    html = """
    <div class="results-container">
      <div class="beer-item">
        <div class="beer-details">
          <p class="name"><a href="/b/foo/1">Foo Beer</a></p>
          <p class="brewery"><a href="/Foo">Foo Brewery</a></p>
        </div>
      </div>
    </div>
    """
    candidates = untappd_search.parse_search_results(html)
    assert len(candidates) == 1
    assert candidates[0].rating is None


def test_parse_handles_zero_rating_as_none():
    html = """
    <div class="results-container">
      <div class="beer-item">
        <div class="beer-details">
          <p class="name"><a href="/b/foo/1">Foo</a></p>
          <p class="brewery"><a href="/Foo">Foo</a></p>
        </div>
        <div class="rating"><div class="caps" data-rating="0.000"></div></div>
      </div>
    </div>
    """
    candidates = untappd_search.parse_search_results(html)
    assert candidates[0].rating is None


def test_search_beer_calls_download_page_with_search_url():
    html = _read_fixture("untappd_search_empty.html")
    with (
        mock.patch.object(untappd_search.common, "download_page", return_value=html) as mock_download,
        mock.patch.object(untappd_search.common, "random_sleep"),
    ):
        untappd_search.search_beer("Tears of St Laurent (2020) Wild Creatures")

    called_url = mock_download.call_args.args[0]
    assert called_url.startswith("https://untappd.com/search?")
    assert "type=beer" in called_url
    assert "Tears" in called_url
