import datetime

from database.auto_init import db
from pivni_valka.stats.common import ChartData, ChartDataset
from pivni_valka.stats.weekly_chart import get_chart_data


def test_get_chart_data():
    today = datetime.date.today().isoformat()

    db.execute(
        "INSERT INTO pivni_valka VALUES (?, 'sejrik', 1), (?, 'mencik2', 2), (?, 'Mates511', 3), (?, 'ominar', 4);",
        (today,) * 4,
    )

    assert get_chart_data() == ChartData(
        labels=[datetime.date.today().strftime("%Y-%W")],
        datasets=[
            ChartDataset(label="Matěj", data=[3], color="#90be6d"),
            ChartDataset(label="Dan", data=[2], color="#43aa8b"),
            ChartDataset(label="Jirka", data=[1], color="#577590"),
        ],
    )
