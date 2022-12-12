import json
import pathlib

from bs4 import BeautifulSoup

import utils
from notifier.base import Beer, Offer


class AmbasadaOffer(Offer):
    BEERS_PATH = "notifier/ambasada.json"
    PUB_IN_NOTIFICATION = "v Ambasádě"

    def run(self) -> None:
        page = utils.download_page("https://pivniambasada.cz")

        self._load_previous_beers()
        self._load_current_beers(page)
        self.new_beers = [
            beer for beer in self._current_beers if beer not in self._previous_beers
        ]

        self._sort_beers()
        self._save_beers()

    def _load_previous_beers(self) -> None:
        path = pathlib.Path(self.BEERS_PATH)

        if not path.exists():
            return

        self._previous_beers = [
            Beer.from_json(beer) for beer in json.loads(path.read_text())["beers"]
        ]

    def _load_current_beers(self, page: str) -> None:
        soup = BeautifulSoup(page, "html.parser")

        table = soup.find_all("table", class_="listek_tab")[0]
        rows = table.find_all("tr")

        beers = []
        current_beer = Beer()

        for row in rows:
            if row.find("td", class_="listek_tab_nadpis"):
                break

            if name := row.find("td", class_="listek_tab_nazev"):
                current_beer.name = name.text.strip()

            if description := row.find("td", class_="listek_tab_popis"):
                current_beer.description = description.text.strip()
                beers.append(current_beer)
                current_beer = Beer()

        self._current_beers = beers

    def _sort_beers(self) -> None:
        self._current_beers.sort(key=lambda beer: beer.name)

    def _save_beers(self) -> None:
        data = {"beers": [beer.to_json() for beer in self._current_beers]}

        with open(self.BEERS_PATH, "w", encoding=utils.ENCODING) as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
