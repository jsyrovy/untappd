import logging
import re
from dataclasses import dataclass

from sqlalchemy import text

from database.orm import engine
from utils import pushover

logger = logging.getLogger(__name__)


@dataclass
class Beer:
    name: str = ""
    description: str = ""
    tasted: bool = False

    def __str__(self) -> str:
        return f"{self.name}{'' if self.tasted else ' 🆕'}\n{self.description}"

    @staticmethod
    def from_json(json_: dict[str, str]) -> Beer:
        return Beer(
            json_["name"],
            json_["description"],
        )

    def to_json(self) -> dict[str, str]:
        return {
            "name": self.name,
            "description": self.description,
        }


class Offer:
    PUB_IN_NOTIFICATION = ""

    def __init__(self) -> None:
        self._previous_beers: list[Beer] = []
        self._current_beers: list[Beer] = []
        self.new_beers: list[Beer] = []

    def run(self) -> None:
        raise NotImplementedError

    def send_notification(self, notificationless: bool) -> None:
        message = f"Nově na čepu {self.PUB_IN_NOTIFICATION}:\n\n"
        message += "\n\n".join(str(beer) for beer in self.new_beers)

        if notificationless:
            logger.info(message)
            return

        pushover.send_notification(message)

    def set_tasted(self) -> None:
        for beer in self.new_beers:
            beer.tasted = is_in_archive(beer)


def is_in_archive(beer: Beer) -> bool:
    def _exists(_beer: str, _brewery: str) -> bool:
        with engine.connect() as conn:
            return bool(
                conn.execute(
                    text(
                        "SELECT 1 FROM `archive` "
                        "WHERE `beer` = :beer COLLATE NOCASE AND `brewery` = :brewery COLLATE NOCASE;",
                    ).bindparams(beer=_beer, brewery=_brewery),
                ).first(),
            )

    if _exists(beer.name, beer.description):
        return True

    cleaned_beer = get_cleaned_beer(beer)
    return _exists(cleaned_beer.name, cleaned_beer.description)


def get_cleaned_beer(beer: Beer) -> Beer:
    name = re.sub(r"\d+°", "", beer.name.lower())
    brewery = beer.description.lower().replace("pivovar", "")

    return Beer(name.strip(), brewery.strip())
