import datetime
from dataclasses import dataclass
from typing import Optional

import utils
from db import Db


@dataclass
class ChartDataset:
    label: str
    data: list[int]
    color: str


@dataclass
class ChartData:
    labels: list[str]
    datasets: list[ChartDataset]


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


class Stats:
    def __init__(self, db: Db) -> None:
        self._db = db

    def save_daily_stats(self, date: datetime.date, user_name: str, count: int):
        exists = self._db.query_one('SELECT 1 FROM pivni_valka WHERE `date` = ? and user = ?;', (date, user_name))

        if exists:
            self._db.execute(
                'UPDATE pivni_valka SET unique_beers = ? WHERE `date` = ? and user = ?;',
                (count, date, user_name),
            )
        else:
            self._db.execute(
                'INSERT INTO pivni_valka (`date`, user, unique_beers) VALUES (?, ?, ?);',
                (date, user_name, count)
            )

        self._db.commit()

    def get_chart_data(self, days: Optional[int] = None) -> ChartData:
        datasets = []

        for user in utils.user.USERS:
            datasets.append(ChartDataset(user.name, self._get_user_data(user.user_name, days), user.color))

        return ChartData(self._get_chart_labels(days), datasets)

    def _get_chart_labels(self, days: Optional[int] = None) -> list[str]:
        sql = 'SELECT DISTINCT `date` FROM pivni_valka ORDER BY `date` DESC'
        labels = self._db.query_all(f'{sql} LIMIT {days};' if days else sql)
        return [label[0] for label in reversed(labels)]

    def _get_user_data(self, user_name: str, days: Optional[int] = None) -> list[int]:
        days = days or self._get_days()
        dates = reversed([datetime.date.today() - datetime.timedelta(days=i) for i in range(days)])
        return [self.get_unique_beers_before(user_name, before=date) for date in dates]

    def get_tiles_data(self) -> list[TileData]:
        tiles_data = []
        total_unique_beers = self.get_total_unique_beers()
        user_with_crown = max(total_unique_beers)

        for user in utils.user.USERS:
            tiles_data.append(TileData(
                user.name,
                user.user_name,
                f'{utils.BASE_URL}/user/{user.user_name}',
                user.color,
                total_unique_beers[user.user_name],
                self.get_unique_beers(user.user_name, days=1, formatted=True),
                self.get_unique_beers(user.user_name, days=7, formatted=True),
                self.get_unique_beers(user.user_name, days=30, formatted=True),
                user.user_name == user_with_crown,
            ))

        return tiles_data

    def get_unique_beers(self, user_name: str, days: Optional[int] = None, formatted: bool = False) -> str:
        sql = 'SELECT unique_beers FROM pivni_valka WHERE user = ? ORDER BY `date` DESC'
        values = self._db.query_all(f'{sql} LIMIT {days};' if days else sql, (user_name,))
        beers = sum(value[0] for value in values)

        if formatted:
            return f'+{beers}' if beers else str(beers)

        return str(beers)

    def get_unique_beers_before(self, user_name: str, before: datetime.date) -> int:
        return self._db.query_one(
            'SELECT SUM(unique_beers) FROM pivni_valka WHERE user = ? AND `date` < ?',
            (user_name, before.isoformat()),
        )[0]

    def _get_days(self) -> int:
        return self._db.query_one('SELECT COUNT(`date`) FROM (SELECT DISTINCT `date` FROM pivni_valka)')[0]

    def get_total_unique_beers(self) -> dict[str, int]:
        return {value[0]: value[1] for value in self._db.query_all(
            'SELECT user, SUM(unique_beers) FROM pivni_valka GROUP BY user;'
        )}
