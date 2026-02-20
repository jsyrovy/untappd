import itertools

from sqlalchemy import select
from sqlalchemy.orm import Session

import utils.user
from database.models import PivniValka
from database.orm import engine
from pivni_valka.stats.common import ChartData, ChartDataset


def get_all_chart_data() -> ChartData:
    labels = _get_all_chart_labels()
    datasets = [
        ChartDataset(user.name, _get_user_cumulative(user.user_name), user.color) for user in utils.user.VISIBLE_USERS
    ]
    return ChartData(labels, datasets)


def slice_chart_data(full_data: ChartData, days: int) -> ChartData:
    return ChartData(
        labels=full_data.labels[-days:],
        datasets=[ChartDataset(label=ds.label, data=ds.data[-days:], color=ds.color) for ds in full_data.datasets],
    )


def get_user_cumulative(user_name: str, days: int | None = None) -> list[int]:
    cumulative = _get_user_cumulative(user_name)
    if days is not None:
        return cumulative[-days:]
    return cumulative


def _get_user_cumulative(user_name: str) -> list[int]:
    stmt = select(PivniValka.unique_beers).where(PivniValka.user == user_name).order_by(PivniValka.date)

    with Session(engine) as session:
        values = session.execute(stmt).scalars().all()

    return list(itertools.accumulate(values))


def _get_all_chart_labels() -> list[str]:
    stmt = select(PivniValka.date).distinct().order_by(PivniValka.date)

    with Session(engine) as session:
        dates = session.execute(stmt).scalars().all()

    return [date.isoformat() for date in dates]
