from dataclasses import dataclass

import utils
from pivni_valka.stats.common import get_total_unique_beers, get_unique_beers


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
    user_with_crown = max(total_unique_beers)

    for user in utils.user.USERS:
        tiles_data.append(
            TileData(
                user.name,
                user.user_name,
                f"{utils.BASE_URL}/user/{user.user_name}",
                user.color,
                total_unique_beers[user.user_name],
                get_unique_beers(user.user_name, days=1, formatted=True),
                get_unique_beers(user.user_name, days=7, formatted=True),
                get_unique_beers(user.user_name, days=30, formatted=True),
                user.user_name == user_with_crown,
            )
        )

    return tiles_data
