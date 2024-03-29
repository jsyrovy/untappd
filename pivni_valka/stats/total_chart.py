import datetime
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

import utils.user
from database.models import PivniValka
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
    inner_stmt = select(PivniValka.date).distinct()
    subquery = inner_stmt.subquery()
    stmt = select(func.count(subquery.c.date))  # pylint: disable=not-callable

    with Session(engine) as session:
        return session.execute(stmt).scalar_one()


def _get_chart_labels(days: Optional[int] = None) -> list[str]:
    stmt = select(PivniValka.date).distinct().order_by(PivniValka.date.desc())

    if days:
        stmt = stmt.limit(days)

    with Session(engine) as session:
        dates = session.execute(stmt).scalars().all()

    return [date.isoformat() for date in reversed(dates)]
