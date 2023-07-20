import datetime
from dataclasses import dataclass
from typing import Optional

from sqlalchemy import text, func, select
from sqlalchemy.orm import Session

from database.models import PivniValka
from database.orm import engine


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
    with engine.connect() as conn:
        return {
            value[0]: value[1]
            for value in conn.execute(
                text("SELECT user, SUM(unique_beers) FROM pivni_valka GROUP BY user;")
            ).all()
        }


def get_unique_beers(
    user_name: str, days: Optional[int] = None, formatted: bool = False
) -> str:
    sql = "SELECT unique_beers FROM pivni_valka WHERE user = :user ORDER BY `date` DESC"
    with engine.connect() as conn:
        values = (
            conn.execute(
                text(f"{sql} LIMIT {days};" if days else sql).bindparams(user=user_name)
            )
            .scalars()
            .all()
        )

    beers = sum(values)

    if formatted:
        return f"+{beers}" if beers else str(beers)

    return str(beers)


def get_unique_beers_before(user_name: str, before: datetime.date) -> int:
    stmt = select(func.sum(PivniValka.unique_beers)).where(  # pylint: disable=not-callable
        PivniValka.user == user_name, PivniValka.date < before
    )
    with Session(engine) as session:
        return session.execute(stmt).scalar_one()  # type: ignore[no-any-return]


def save_daily_stats(date: datetime.date, user_name: str, count: int) -> None:
    with engine.connect() as conn:
        exists = bool(
            conn.execute(
                text(
                    "SELECT 1 FROM pivni_valka WHERE `date` = :date and user = :user;",
                ).bindparams(date=date, user=user_name)
            ).first()
        )

        if exists:
            conn.execute(
                text(
                    "UPDATE pivni_valka SET unique_beers = :unique_beers WHERE `date` = :date and user = :user;",
                ).bindparams(date=date, user=user_name, unique_beers=count)
            )
        else:
            conn.execute(
                text(
                    "INSERT INTO pivni_valka (`date`, user, unique_beers) VALUES (:date, :user, :unique_beers);",
                ).bindparams(date=date, user=user_name, unique_beers=count)
            )

        conn.commit()
