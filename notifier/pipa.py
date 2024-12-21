import json
import pathlib
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from hospody import CHECK_INS_PATH
from notifier.base import Beer, Offer
from utils import common


@dataclass
class PipaBeer(Beer):
    dt: datetime = datetime.now()

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PipaBeer):
            return False

        return self.name == other.name and self.description == other.description

    @staticmethod
    def from_json(json_: dict[str, str]) -> "PipaBeer":
        return PipaBeer(
            name=json_["beer_name"],
            description=json_["brewery"],
            tasted=False,
            dt=datetime.fromisoformat(json_["dt"]),
        )


class PipaOffer(Offer):
    PUB_IN_NOTIFICATION = "v Pípě"
    PUB_NAME = common.PIPA_NAME

    def run(self) -> None:
        self._load_beers()

    def _load_beers(self) -> None:
        path = pathlib.Path(CHECK_INS_PATH)

        if not path.exists():
            return

        beers = [
            PipaBeer.from_json(check_in)
            for check_in in json.loads(path.read_text(common.ENCODING))["check_ins"]
            if check_in["venue_name"] == self.PUB_NAME
        ]

        now = datetime.now(tz=timezone(timedelta(seconds=7200)))

        self._previous_beers = list(
            {beer for beer in beers if now - timedelta(days=3) < beer.dt < now - timedelta(days=1)},
        )
        self._current_beers = list({beer for beer in beers if beer.dt > now - timedelta(days=1)})
        self.new_beers = [beer for beer in self._current_beers if beer not in self._previous_beers]


class LodOffer(PipaOffer):
    PUB_IN_NOTIFICATION = "na Lodi"
    PUB_NAME = common.LOD_NAME
