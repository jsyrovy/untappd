import datetime
from typing import Optional

import utils
from db import db
from pivni_valka.stats.common import ChartData, ChartDataset, get_unique_beers_before


def get_chart_data(days: int) -> ChartData:
    datasets = []

    for user in utils.user.USERS:
        if user.user_name in ('Mates511', 'sejrik', 'mencik2'):
            datasets.append(ChartDataset(user.name, _get_user_data(user.user_name, days), user.color))

    dataset_jirka = datasets[0]
    dataset_dan = datasets[1]
    dataset_matej = datasets[2]

    for i, value in enumerate(dataset_matej.data):
        dataset_jirka.data[i] -= value
        dataset_dan.data[i] -= value

    return ChartData(_get_chart_labels(days), [dataset_jirka, dataset_dan])


def _get_chart_labels(days: Optional[int] = None) -> list[str]:
    sql = 'SELECT DISTINCT `date` FROM pivni_valka ORDER BY `date` DESC'
    labels = db.query_all(f'{sql} LIMIT {days};' if days else sql)
    return [label[0] for label in reversed(labels)]


def _get_user_data(user_name: str, days: Optional[int] = None) -> list[int]:
    dates = reversed([datetime.date.today() - datetime.timedelta(days=i) for i in range(days)])
    return [get_unique_beers_before(user_name, before=date) for date in dates]
