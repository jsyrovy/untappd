import json
import random
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import jinja2
from bs4 import BeautifulSoup

from robot.base import BaseRobot
from utils import common

CHECK_INS_PATH = "hospody/check_ins.json"

SERVING_DRAFT = "Čepované"
SERVING_BOTTLE = "Lahvové"
SERVING_CAN = "Plechovkové"
SERVING_UNKNOWN = "Nezadáno"


@dataclass
class Venue:
    name: str
    url: str


@dataclass
class CheckIn:
    id: int
    dt: datetime
    venue_name: str
    beer_name: str
    brewery: str
    serving: str
    beer_link: str
    venue_link: str

    @staticmethod
    def get_random(venues: tuple[Venue, ...]) -> "CheckIn":
        return CheckIn(
            random.randrange(1000),
            datetime.now(tz=timezone(timedelta(seconds=7200))),
            random.choice(venues).name,
            "Pivo",
            "Pivovar",
            SERVING_DRAFT,
            common.BASE_URL,
            random.choice(venues).url,
        )

    @staticmethod
    def from_json(json_: dict[str, Any], venues: tuple[Venue, ...]) -> "CheckIn":
        return CheckIn(
            json_["id"],
            datetime.fromisoformat(json_["dt"]),
            json_["venue_name"],
            json_["beer_name"],
            json_["brewery"],
            json_["serving"],
            json_["beer_link"],
            next(venue.url for venue in venues if venue.name == json_["venue_name"]),
        )

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "dt": self.dt.isoformat(),
            "venue_name": self.venue_name,
            "beer_name": self.beer_name,
            "brewery": self.brewery,
            "serving": self.serving,
            "beer_link": self.beer_link,
        }


class Hospody(BaseRobot):
    def _main(self) -> None:
        venues = (
            Venue(common.PIPA_NAME, f"{common.BASE_URL}/v/u-toulave-pipy/3663231"),
            Venue(common.AMBASADA_NAME, f"{common.BASE_URL}/v/pivni-ambasada/3943799"),
            Venue(common.LOD_NAME, f"{common.BASE_URL}/v/lod-otava/6353222"),
        )

        new_check_ins = []

        for venue in venues:
            new_check_ins.extend(get_new_check_ins(self._args.local, venue, venues))
            common.random_sleep()

        check_ins = load_check_ins(venues)

        for new_check_in in new_check_ins:
            if new_check_in in check_ins:
                print(f"Check in {new_check_in.id} jiz existuje.")
                continue

            check_ins.append(new_check_in)
            print(f"Novy check in {new_check_in.id} - {new_check_in.beer_name}.")

        sort_check_ins(check_ins)
        save_check_ins(check_ins)
        unique_beers_check_ins = get_unique_beers_check_ins(check_ins)
        page = get_page(common.get_template("hospody.html"), unique_beers_check_ins)

        with Path("web/hospody/index.html").open("w") as f:
            f.write(page)


def get_new_check_ins(local: bool, venue: Venue, venues: tuple[Venue, ...]) -> list[CheckIn]:
    if local:
        return [
            CheckIn.get_random(venues),
            CheckIn.get_random(venues),
            CheckIn.get_random(venues),
        ]

    page = common.download_page(venue.url)
    return parse_check_ins(page, venue)


def parse_check_ins(page: str, venue: Venue) -> list[CheckIn]:
    def parse_dt(dt_as_string: str) -> datetime:
        utc_dt = datetime.strptime(dt_as_string, "%a, %d %b %Y %H:%M:%S %z")
        return utc_dt.replace(tzinfo=UTC).astimezone(tz=None)

    def get_czech_serving(en_serving: str) -> str:
        return {
            "Draft": SERVING_DRAFT,
            "Bottle": SERVING_BOTTLE,
            "Can": SERVING_CAN,
            None: SERVING_UNKNOWN,
        }.get(en_serving, en_serving)

    soup = BeautifulSoup(page, "html.parser")

    main_stream = soup.find("div", id="main-stream")
    items = main_stream.find_all("div", class_="item")

    beers = []

    for item in items:
        check_in = item.find("div", class_="checkin")
        text = check_in.find("p", class_="text")
        links = text.find_all("a")
        checkin_comment = check_in.find("div", class_="checkin-comment")
        feedback = check_in.find("div", class_="feedback")

        id_ = int(item["data-checkin-id"])
        dt = parse_dt(feedback.find("a", class_="time").text)
        beer_name = links[1].text
        brewery = links[2].text
        serving_section = checkin_comment.find("p", class_="serving") if checkin_comment else None
        serving = get_czech_serving(serving_section.find("span").text if serving_section else "")
        beer_link = f"{common.BASE_URL}{links[1]['href']}"

        beers.append(CheckIn(id_, dt, venue.name, beer_name, brewery, serving, beer_link, venue.url))

    return beers


def load_check_ins(venues: tuple[Venue, ...]) -> list[CheckIn]:
    path = Path(CHECK_INS_PATH)

    if not path.exists():
        return []

    return [
        CheckIn.from_json(check_in, venues)
        for check_in in json.loads(path.read_text(encoding=common.ENCODING))["check_ins"]
    ]


def sort_check_ins(check_ins: list[CheckIn]) -> None:
    check_ins.sort(key=lambda check_in: check_in.dt, reverse=True)


def save_check_ins(check_ins: list[CheckIn]) -> None:
    data = {"check_ins": [check_in.to_json() for check_in in check_ins]}

    with Path(CHECK_INS_PATH).open("w") as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))


def get_unique_beers_check_ins(check_ins: list[CheckIn]) -> list[CheckIn]:
    unique_beers_check_ins: list[CheckIn] = []

    for check_in in [check_in for check_in in check_ins if check_in.serving in (SERVING_DRAFT, SERVING_UNKNOWN)]:
        if check_in.beer_name not in [
            unique_beers_checkin.beer_name for unique_beers_checkin in unique_beers_check_ins
        ]:
            unique_beers_check_ins.append(check_in)

    return unique_beers_check_ins


def get_page(template: jinja2.Template, check_ins: list[CheckIn]) -> str:
    return template.render(check_ins=check_ins)
