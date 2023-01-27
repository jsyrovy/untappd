from db import use_fresh_test_db
from pivni_valka.stats.common import ChartData, ChartDataset
from pivni_valka.stats.matej_chart import get_chart_data


@use_fresh_test_db
def test_get_chart_data():
    assert get_chart_data(1) == ChartData(
        labels=['2022-01-04'],
        datasets=[
            ChartDataset(label='Jirka', data=[-22], color='#577590'),
            ChartDataset(label='Dan', data=[-11], color='#43aa8b'),
        ],
    )
