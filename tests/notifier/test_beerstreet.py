import json
from unittest import mock

from notifier.base import Beer
from notifier.beerstreet import BeerStreetOffer

BEERSTREET_JSON = json.dumps(
    {
        "beers": [
            {
                "epm": "12",
                "nazev": "  Loutkář  ",
                "nazev_pivovaru": "  Loutkář  ",
                "styl": "Ležák světlý",
                "avb": 4.8,
                "cena04": 59,
                "cena03": "",
            },
            {
                "epm": "11",
                "nazev": "Vinohradská",
                "nazev_pivovaru": "Vinohradský pivovar",
                "styl": "Ležák světlý",
                "avb": 4.5,
                "cena04": 59,
                "cena03": "",
            },
        ],
    },
    ensure_ascii=False,
)

PREVIOUS_BEERS_JSON = json.dumps(
    {
        "beers": [
            {"name": "12° Loutkář", "description": "4.8% alc., Loutkář, Ležák světlý"},
        ],
    },
    ensure_ascii=False,
)


def test_load_current_beers():
    offer = BeerStreetOffer()
    offer._load_current_beers(BEERSTREET_JSON)

    assert len(offer._current_beers) == 2
    assert offer._current_beers[0].name == "12° Loutkář"
    assert offer._current_beers[0].description == "4.8% alc., Loutkář, Ležák světlý"
    assert offer._current_beers[1].name == "11° Vinohradská"
    assert offer._current_beers[1].description == "4.5% alc., Vinohradský pivovar, Ležák světlý"


def test_load_current_beers_missing_fields():
    data = json.dumps({"beers": [{"nazev": "Test Beer"}]})

    offer = BeerStreetOffer()
    offer._load_current_beers(data)

    assert len(offer._current_beers) == 1
    assert offer._current_beers[0].name == "Test Beer"
    assert offer._current_beers[0].description == ""


def test_load_current_beers_partial_fields():
    data = json.dumps({"beers": [{"nazev": "Test", "nazev_pivovaru": "Brewery", "epm": "11"}]})

    offer = BeerStreetOffer()
    offer._load_current_beers(data)

    assert offer._current_beers[0].name == "11° Test"
    assert offer._current_beers[0].description == "Brewery"


def test_load_previous_beers_file_exists(tmp_path):
    beers_file = tmp_path / "beerstreet.json"
    beers_file.write_text(PREVIOUS_BEERS_JSON)

    offer = BeerStreetOffer()
    offer.BEERS_PATH = str(beers_file)
    offer._load_previous_beers()

    assert len(offer._previous_beers) == 1
    assert offer._previous_beers[0].name == "12° Loutkář"


def test_load_previous_beers_file_missing(tmp_path):
    offer = BeerStreetOffer()
    offer.BEERS_PATH = str(tmp_path / "nonexistent.json")
    offer._load_previous_beers()

    assert offer._previous_beers == []


def test_sort_beers():
    offer = BeerStreetOffer()
    offer._current_beers = [
        Beer("11° Vinohradská", "4.5% alc., Vinohradský pivovar, Ležák světlý"),
        Beer("12° Loutkář", "4.8% alc., Loutkář, Ležák světlý"),
    ]
    offer._sort_beers()

    assert offer._current_beers[0].name == "11° Vinohradská"
    assert offer._current_beers[1].name == "12° Loutkář"


def test_save_beers(tmp_path):
    beers_file = tmp_path / "beerstreet.json"

    offer = BeerStreetOffer()
    offer.BEERS_PATH = str(beers_file)
    offer._current_beers = [Beer("12° IPA", "5% alc., Brewery, Pale Ale")]
    offer._save_beers()

    data = json.loads(beers_file.read_text())
    assert data == {"beers": [{"name": "12° IPA", "description": "5% alc., Brewery, Pale Ale"}]}


def test_run(tmp_path):
    beers_file = tmp_path / "beerstreet.json"
    beers_file.write_text(PREVIOUS_BEERS_JSON)

    offer = BeerStreetOffer()
    offer.BEERS_PATH = str(beers_file)

    with mock.patch("notifier.beerstreet.common.download_page", return_value=BEERSTREET_JSON):
        offer.run()

    assert len(offer._current_beers) == 2
    assert len(offer.new_beers) == 1
    assert offer.new_beers[0].name == "11° Vinohradská"
    assert offer.new_beers[0].description == "4.5% alc., Vinohradský pivovar, Ležák světlý"

    saved_data = json.loads(beers_file.read_text())
    assert len(saved_data["beers"]) == 2
