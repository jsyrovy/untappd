from dataclasses import dataclass
from operator import itemgetter

import utils.user
from pivni_valka.stats.common import get_total_unique_beers, get_unique_beers
from utils import common


@dataclass
class TileData:
    name: str
    user_name: str
    url: str
    color: str
    unique_beers_count: int
    diff_day: str
    diff_week: str
    diff_month: str
    has_crown: bool


def get_tiles_data() -> list[TileData]:
    tiles_data = []
    total_unique_beers = get_total_unique_beers()
    user_with_crown = max(total_unique_beers.items(), key=itemgetter(1))[0]

    for user in utils.user.VISIBLE_USERS:
        tiles_data.append(
            TileData(
                user.name,
                user.user_name,
                f"{common.BASE_URL}/user/{user.user_name}",
                user.color,
                total_unique_beers[user.user_name],
                get_unique_beers(user.user_name, days=1, formatted=True),
                get_unique_beers(user.user_name, days=7, formatted=True),
                get_unique_beers(user.user_name, days=30, formatted=True),
                user.user_name == user_with_crown,
            ),
        )

    return tiles_data
