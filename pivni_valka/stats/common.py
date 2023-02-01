import datetime
from dataclasses import dataclass
from typing import Optional

from database import db


@dataclass
class ChartDataset:
    label: str
    data: list[int]
    color: str


@dataclass
class ChartData:
    labels: list[str]
    datasets: list[ChartDataset]


def get_total_unique_beers() -> dict[str, int]:
    return {
        value[0]: value[1]
        for value in db.query_all(
            "SELECT user, SUM(unique_beers) FROM pivni_valka GROUP BY user;"
        )
    }


def get_unique_beers(
    user_name: str, days: Optional[int] = None, formatted: bool = False
) -> str:
    sql = "SELECT unique_beers FROM pivni_valka WHERE user = ? ORDER BY `date` DESC"
    values = db.query_all(f"{sql} LIMIT {days};" if days else sql, (user_name,))
    beers = sum(value[0] for value in values)

    if formatted:
        return f"+{beers}" if beers else str(beers)

    return str(beers)


def get_unique_beers_before(user_name: str, before: datetime.date) -> int:
    return db.query_one(
        "SELECT SUM(unique_beers) FROM pivni_valka WHERE user = ? AND `date` < ?",
        (user_name, before.isoformat()),
    )[0]


def save_daily_stats(date: datetime.date, user_name: str, count: int):
    exists = db.query_one(
        "SELECT 1 FROM pivni_valka WHERE `date` = ? and user = ?;", (date, user_name)
    )

    if exists:
        db.execute(
            "UPDATE pivni_valka SET unique_beers = ? WHERE `date` = ? and user = ?;",
            (count, date, user_name),
        )
    else:
        db.execute(
            "INSERT INTO pivni_valka (`date`, user, unique_beers) VALUES (?, ?, ?);",
            (date, user_name, count),
        )

    db.commit()
