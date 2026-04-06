import json
import logging
from pathlib import Path

from notifier.base import Beer, Offer
from utils import common

logger = logging.getLogger(__name__)


class BeerStreetOffer(Offer):
    BEERS_PATH = "notifier/beerstreet.json"
    PUB_IN_NOTIFICATION = "v Beer Streetu"

    def run(self) -> None:
        page = common.download_page("https://beerstreet.cz/data/beers.json")

        self._load_previous_beers()
        self._load_current_beers(page)
        self.new_beers = [beer for beer in self._current_beers if beer not in self._previous_beers]

        self._sort_beers()
        self._save_beers()

    def _load_previous_beers(self) -> None:
        path = Path(self.BEERS_PATH)

        if not path.exists():
            return

        self._previous_beers = [Beer.from_json(beer) for beer in json.loads(path.read_text(common.ENCODING))["beers"]]

    def _load_current_beers(self, page: str) -> None:
        data = json.loads(page)

        self._current_beers = [
            Beer(name=self._build_name(beer), description=self._build_description(beer)) for beer in data["beers"]
        ]

    @staticmethod
    def _build_name(beer: dict[str, str | float]) -> str:
        epm = str(beer.get("epm", "")).strip()
        name = str(beer.get("nazev", "")).strip()

        if epm:
            return f"{epm}° {name}"
        return name

    @staticmethod
    def _build_description(beer: dict[str, str | float]) -> str:
        parts: list[str] = []

        abv = str(beer.get("avb", "")).strip()
        if abv:
            parts.append(f"{abv}% alc.")

        brewery = str(beer.get("nazev_pivovaru", "")).strip()
        if brewery:
            parts.append(brewery)

        style = str(beer.get("styl", "")).strip()
        if style:
            parts.append(style)

        return ", ".join(parts)

    def _sort_beers(self) -> None:
        self._current_beers.sort(key=lambda beer: beer.name)

    def _save_beers(self) -> None:
        data = {"beers": [beer.to_json() for beer in self._current_beers]}

        with Path(self.BEERS_PATH).open("w") as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
