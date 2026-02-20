import itertools

from sqlalchemy import select
from sqlalchemy.orm import Session

import utils.user
from database.models import PivniValka
from database.orm import engine
from pivni_valka.stats.common import ChartData, ChartDataset


def get_chart_data(days: int | None = None) -> ChartData:
    datasets = [
        ChartDataset(user.name, _get_user_data(user.user_name, days), user.color) for user in utils.user.VISIBLE_USERS
    ]
    return ChartData(_get_chart_labels(days), datasets)


def _get_user_data(user_name: str, days: int | None = None) -> list[int]:
    stmt = (
        select(PivniValka.date, PivniValka.unique_beers).where(PivniValka.user == user_name).order_by(PivniValka.date)
    )

    with Session(engine) as session:
        rows = session.execute(stmt).all()

    cumulative = list(itertools.accumulate(row.unique_beers for row in rows))

    if days is not None:
        return cumulative[-days:]

    return cumulative


def _get_chart_labels(days: int | None = None) -> list[str]:
    stmt = select(PivniValka.date).distinct().order_by(PivniValka.date.desc())

    if days:
        stmt = stmt.limit(days)

    with Session(engine) as session:
        dates = session.execute(stmt).scalars().all()

    return [date.isoformat() for date in reversed(dates)]
