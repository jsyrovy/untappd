import datetime
from typing import Optional

from sqlalchemy import text

import utils
from database.orm import engine
from pivni_valka.stats.common import ChartData, ChartDataset, get_unique_beers_before


def get_chart_data(days: Optional[int] = None) -> ChartData:
    datasets = []

    for user in utils.user.VISIBLE_USERS:
        datasets.append(ChartDataset(user.name, _get_user_data(user.user_name, days), user.color))

    return ChartData(_get_chart_labels(days), datasets)


def _get_user_data(user_name: str, days: Optional[int] = None) -> list[int]:
    days = days or _get_days()
    dates = reversed([datetime.date.today() - datetime.timedelta(days=i) for i in range(days)])
    return [get_unique_beers_before(user_name, before=date) for date in dates]


def _get_days() -> int:
    with engine.connect() as conn:
        return conn.execute(  # type: ignore
            text("SELECT COUNT(`date`) FROM (SELECT DISTINCT `date` FROM pivni_valka)")
        ).scalar_one()


def _get_chart_labels(days: Optional[int] = None) -> list[str]:
    sql = "SELECT DISTINCT `date` FROM pivni_valka ORDER BY `date` DESC"
    with engine.connect() as conn:
        return list(reversed(conn.execute(text(f"{sql} LIMIT {days};" if days else sql)).scalars().all()))
