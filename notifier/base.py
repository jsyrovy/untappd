from dataclasses import dataclass

import utils
from database.auto_init import db


@dataclass
class Beer:
    name: str = ""
    description: str = ""
    tasted: bool = False

    def __str__(self) -> str:
        return f"{self.name}{'' if self.tasted else ' 🆕'}\n{self.description}"

    @staticmethod
    def from_json(json_: dict[str, str]) -> "Beer":
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

    def send_twitter_message(self, tweetless: bool) -> None:
        message = f"Nově na čepu {self.PUB_IN_NOTIFICATION}:\n\n"
        message += "\n\n".join(str(beer) for beer in self.new_beers)

        if tweetless:
            print(message)
            return

        twitter_client = utils.twitter.Client()
        twitter_client.send_message(message)

    def set_tasted(self) -> None:
        for beer in self.new_beers:
            beer.tasted = is_in_archive(beer)


def is_in_archive(beer: Beer) -> bool:
    return bool(
        db.query_one(
            "SELECT 1 FROM `archive` WHERE `beer` = ? AND `brewery` = ?;",
            (beer.name, beer.description),
        )
    )
