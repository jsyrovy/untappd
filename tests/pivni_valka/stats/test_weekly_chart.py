import datetime

from sqlalchemy import text

from database.orm import engine
from pivni_valka.stats.common import ChartData, ChartDataset
from pivni_valka.stats.weekly_chart import get_chart_data


def test_get_chart_data():
    today = datetime.date.today().isoformat()

    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO pivni_valka (date, user, unique_beers) "
                "VALUES (:date, 'sejrik', 1), (:date, 'mencik2', 2), (:date, 'Mates511', 3), (:date, 'ominar', 4);",
            ).bindparams(date=today)
        )
        conn.commit()

    assert get_chart_data() == ChartData(
        labels=[datetime.date.today().strftime("%Y-%W")],
        datasets=[
            ChartDataset(label="Matěj", data=[3], color="#90be6d"),
            ChartDataset(label="Dan", data=[2], color="#43aa8b"),
            ChartDataset(label="Jirka", data=[1], color="#577590"),
        ],
    )
