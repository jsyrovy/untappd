import datetime
from dataclasses import dataclass
from typing import Optional

import utils


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


def save_daily_stats(date: datetime.date, user_name: str, count: int, db: utils.db.Db):
    db.cur.execute('SELECT 1 FROM pivni_valka WHERE `date` = ? and user = ?;', (date, user_name))
    exists = db.cur.fetchone()

    if exists:
        db.cur.execute(
            'UPDATE pivni_valka SET unique_beers = ? WHERE `date` = ? and user = ?;',
            (count, date, user_name),
        )
    else:
        db.cur.execute(
            'INSERT INTO pivni_valka (`date`, user, unique_beers) VALUES (?, ?, ?);',
            (date, user_name, count)
        )

    db.con.commit()


def get_chart_data(db: utils.db.Db, days: Optional[int] = None) -> ChartData:
    datasets = []

    for user in utils.user.USERS:
        datasets.append(ChartDataset(user.name, _get_user_data(user.user_name, db, days), user.color))

    return ChartData(_get_chart_labels(db, days), datasets)


def _get_chart_labels(db: utils.db.Db, days: Optional[int] = None) -> list[str]:
    sql = 'SELECT DISTINCT `date` FROM pivni_valka ORDER BY `date` DESC'
    db.cur.execute(f'{sql} LIMIT {days};' if days else sql)
    labels = db.cur.fetchall()
    return [label[0] for label in reversed(labels)]


def _get_user_data(user_name: str, db: utils.db.Db, days: Optional[int] = None) -> list[int]:
    days = days or _get_days(db)
    dates = reversed([datetime.date.today() - datetime.timedelta(days=i) for i in range(days)])
    return [get_unique_beers_before(user_name, db, before=date) for date in dates]


def get_tiles_data(db: utils.db.Db) -> list[TileData]:
    tiles_data = []
    total_unique_beers = get_total_unique_beers(db)
    user_with_crown = max(total_unique_beers)

    for user in utils.user.USERS:
        tiles_data.append(TileData(
            user.name,
            user.user_name,
            f'{utils.BASE_URL}/user/{user.user_name}',
            user.color,
            total_unique_beers[user.user_name],
            get_unique_beers(user.user_name, db, days=1, formatted=True),
            get_unique_beers(user.user_name, db, days=7, formatted=True),
            get_unique_beers(user.user_name, db, days=30, formatted=True),
            user.user_name == user_with_crown,
        ))

    return tiles_data


def get_unique_beers(user_name: str, db: utils.db.Db, days: Optional[int] = None, formatted: bool = False) -> str:
    sql = 'SELECT unique_beers FROM pivni_valka WHERE user = ? ORDER BY `date` DESC'
    db.cur.execute(f'{sql} LIMIT {days};' if days else sql, (user_name,))
    values = db.cur.fetchall()
    beers = sum(value[0] for value in values)

    if formatted:
        return f'+{beers}' if beers else str(beers)

    return str(beers)


def get_unique_beers_before(user_name: str, db: utils.db.Db, before: datetime.date) -> int:
    db.cur.execute(
        'SELECT SUM(unique_beers) FROM pivni_valka WHERE user = ? AND `date` < ?',
        (user_name, before.isoformat()),
    )
    return db.cur.fetchone()[0]


def _get_days(db: utils.db.Db) -> int:
    db.cur.execute('SELECT COUNT(`date`) FROM (SELECT DISTINCT `date` FROM pivni_valka)')
    return db.cur.fetchone()[0]


def get_total_unique_beers(db: utils.db.Db) -> dict[str, int]:
    db.cur.execute('SELECT user, SUM(unique_beers) FROM pivni_valka GROUP BY user;')
    return {value[0]: value[1] for value in db.cur.fetchall()}
