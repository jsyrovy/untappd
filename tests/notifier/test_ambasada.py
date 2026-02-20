import json
from unittest import mock

from notifier.ambasada import AmbasadaOffer
from notifier.base import Beer

AMBASADA_HTML = """\
<html>
<body>
<table class="listek_tab">
  <tr>
    <td class="listek_tab_nazev">  Zappa 12°  </td>
  </tr>
  <tr>
    <td class="listek_tab_popis">  Pivovar Falkon  </td>
  </tr>
  <tr>
    <td class="listek_tab_nazev">  AIPA 15°  </td>
  </tr>
  <tr>
    <td class="listek_tab_popis">  Clock  </td>
  </tr>
  <tr>
    <td class="listek_tab_nadpis">Konec</td>
  </tr>
  <tr>
    <td class="listek_tab_nazev">  Ignorovano  </td>
  </tr>
  <tr>
    <td class="listek_tab_popis">  Taky Ignorovano  </td>
  </tr>
</table>
</body>
</html>
"""

PREVIOUS_BEERS_JSON = json.dumps(
    {
        "beers": [
            {"name": "Zappa 12°", "description": "Pivovar Falkon"},
        ],
    },
    ensure_ascii=False,
)


def test_load_current_beers():
    offer = AmbasadaOffer()
    offer._load_current_beers(AMBASADA_HTML)

    assert len(offer._current_beers) == 2
    assert offer._current_beers[0].name == "Zappa 12°"
    assert offer._current_beers[0].description == "Pivovar Falkon"
    assert offer._current_beers[1].name == "AIPA 15°"
    assert offer._current_beers[1].description == "Clock"


def test_load_previous_beers_file_exists(tmp_path):
    beers_file = tmp_path / "ambasada.json"
    beers_file.write_text(PREVIOUS_BEERS_JSON)

    offer = AmbasadaOffer()
    offer.BEERS_PATH = str(beers_file)
    offer._load_previous_beers()

    assert len(offer._previous_beers) == 1
    assert offer._previous_beers[0].name == "Zappa 12°"


def test_load_previous_beers_file_missing(tmp_path):
    offer = AmbasadaOffer()
    offer.BEERS_PATH = str(tmp_path / "nonexistent.json")
    offer._load_previous_beers()

    assert offer._previous_beers == []


def test_sort_beers():
    offer = AmbasadaOffer()
    offer._current_beers = [
        Beer("Zappa 12°", "Falkon"),
        Beer("AIPA 15°", "Clock"),
    ]
    offer._sort_beers()

    assert offer._current_beers[0].name == "AIPA 15°"
    assert offer._current_beers[1].name == "Zappa 12°"


def test_save_beers(tmp_path):
    beers_file = tmp_path / "ambasada.json"

    offer = AmbasadaOffer()
    offer.BEERS_PATH = str(beers_file)
    offer._current_beers = [Beer("IPA", "Brewery")]
    offer._save_beers()

    data = json.loads(beers_file.read_text())
    assert data == {"beers": [{"name": "IPA", "description": "Brewery"}]}


def test_run(tmp_path):
    beers_file = tmp_path / "ambasada.json"
    beers_file.write_text(PREVIOUS_BEERS_JSON)

    offer = AmbasadaOffer()
    offer.BEERS_PATH = str(beers_file)

    with mock.patch("notifier.ambasada.common.download_page", return_value=AMBASADA_HTML):
        offer.run()

    assert len(offer._current_beers) == 2
    assert len(offer.new_beers) == 1
    assert offer.new_beers[0].name == "AIPA 15°"

    saved_data = json.loads(beers_file.read_text())
    assert len(saved_data["beers"]) == 2
