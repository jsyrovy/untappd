import datetime
from collections import OrderedDict

import utils
from db import db
from pivni_valka.stats.common import ChartData, ChartDataset


def _get_week_stats() -> dict[str, dict[str, int]]:
    since = (datetime.date.today() - datetime.timedelta(weeks=12)).strftime("%Y-%W")
    result: dict[str, dict[str, int]] = {}
    stats = db.query_all(
        """
            SELECT strftime('%Y-%W', `date`) as week, user, sum(unique_beers)
            FROM pivni_valka
            WHERE week >= ?
            GROUP BY week, user
            ORDER BY week
        """,
        (since,),
    )

    for week, user_name, beers in stats:
        result.setdefault(user_name, OrderedDict())[week] = beers

    return result


def get_chart_data() -> ChartData:
    datasets = []
    labels: list[str] = []

    for user_name, stats in _get_week_stats().items():
        if user_name not in utils.user.VISIBLE_USER_NAMES:
            continue

        labels = labels or list(stats.keys())
        user = utils.user.get(user_name)
        datasets.append(ChartDataset(user.name, list(stats.values()), user.color))

    return ChartData(labels, datasets)
