from dataclasses import dataclass

import utils


@dataclass
class Beer:
    name: str = ""
    description: str = ""

    def __str__(self) -> str:
        return f"{self.name}\n{self.description}"

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

    def send_twitter_message(self) -> None:
        message = f"Nově na čepu {self.PUB_IN_NOTIFICATION}:\n\n"
        message += "\n\n".join(str(beer) for beer in self.new_beers)

        twitter_client = utils.twitter.Client()
        twitter_client.send_message(message)
