import json
from unittest import mock

import httpx

from robot.base import Args
from untappd_pairing import pairing
from untappd_pairing.pairing import UntappdPairing
from untappd_pairing.tap_api import TapBeer
from untappd_pairing.untappd_search import UntappdCandidate


def _beer(name, brewery="Falkon"):
    return TapBeer(name=name, brewery=brewery, style="IPA", abv=5.0, source="beerstreet")


def _candidate(name, brewery="Falkon", url="https://untappd.com/b/x/1", rating=4.1):
    return UntappdCandidate(name=name, brewery=brewery, url=url, rating=rating)


def test_pairing_writes_matched_and_unmatched(tmp_path, monkeypatch):
    pairings_path = tmp_path / "pairings.json"
    monkeypatch.setattr(pairing, "PAIRINGS_PATH", pairings_path)

    beers = [_beer("Tears of St Laurent (2020)", "Wild Creatures"), _beer("Mystery Brew", "Unknown")]

    def fake_search(query):
        if "Tears" in query:
            return [_candidate("Tears of St Laurent (2020)", brewery="Wild Creatures")]
        return []

    with (
        mock.patch.object(pairing.tap_api, "fetch_all_beers", return_value=beers),
        mock.patch.object(pairing.untappd_search, "search_beer", side_effect=fake_search),
    ):
        UntappdPairing(args=Args()).run()

    saved = json.loads(pairings_path.read_text())
    assert "beerstreet::Wild Creatures::Tears of St Laurent (2020)" in saved["pairings"]
    assert "beerstreet::Unknown::Mystery Brew" in saved["unmatched"]
    assert saved["unmatched"]["beerstreet::Unknown::Mystery Brew"]["reason"] == "no_candidates_above_threshold"


def test_pairing_skips_already_paired_beers_on_second_run(tmp_path, monkeypatch):
    pairings_path = tmp_path / "pairings.json"
    monkeypatch.setattr(pairing, "PAIRINGS_PATH", pairings_path)

    beer = _beer("Tears of St Laurent (2020)", "Wild Creatures")
    candidates = [_candidate("Tears of St Laurent (2020)", brewery="Wild Creatures")]

    search_mock = mock.Mock(return_value=candidates)

    with (
        mock.patch.object(pairing.tap_api, "fetch_all_beers", return_value=[beer]),
        mock.patch.object(pairing.untappd_search, "search_beer", search_mock),
    ):
        UntappdPairing(args=Args()).run()
        UntappdPairing(args=Args()).run()

    assert search_mock.call_count == 1


def test_pairing_records_upstream_error_on_http_failure(tmp_path, monkeypatch):
    pairings_path = tmp_path / "pairings.json"
    monkeypatch.setattr(pairing, "PAIRINGS_PATH", pairings_path)

    beer = _beer("IPA", "Brewery")

    with (
        mock.patch.object(pairing.tap_api, "fetch_all_beers", return_value=[beer]),
        mock.patch.object(
            pairing.untappd_search,
            "search_beer",
            side_effect=httpx.ConnectError("boom"),
        ),
    ):
        UntappdPairing(args=Args()).run()

    saved = json.loads(pairings_path.read_text())
    entry = saved["unmatched"]["beerstreet::Brewery::IPA"]
    assert entry["reason"] == "upstream_error"


def test_pairing_local_mode_skips_network(tmp_path, monkeypatch):
    pairings_path = tmp_path / "pairings.json"
    monkeypatch.setattr(pairing, "PAIRINGS_PATH", pairings_path)

    fetch_mock = mock.Mock()
    search_mock = mock.Mock()

    with (
        mock.patch.object(pairing.tap_api, "fetch_all_beers", fetch_mock),
        mock.patch.object(pairing.untappd_search, "search_beer", search_mock),
    ):
        UntappdPairing(args=Args(local=True)).run()

    fetch_mock.assert_not_called()
    search_mock.assert_not_called()
    assert pairings_path.exists()
