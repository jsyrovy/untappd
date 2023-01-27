from pivni_valka.stats.common import ChartData, ChartDataset
from pivni_valka.stats.total_chart import get_chart_data


def test_get_chart_data():
    assert get_chart_data(1) == ChartData(
        labels=["2022-01-04"],
        datasets=[
            ChartDataset(label="Jirka", data=[11], color="#577590"),
            ChartDataset(label="Dan", data=[22], color="#43aa8b"),
            ChartDataset(label="Matěj", data=[33], color="#90be6d"),
        ],
    )

    assert get_chart_data() == ChartData(
        labels=["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04"],
        datasets=[
            ChartDataset(label="Jirka", data=[11, 11, 11, 11], color="#577590"),
            ChartDataset(label="Dan", data=[22, 22, 22, 22], color="#43aa8b"),
            ChartDataset(label="Matěj", data=[33, 33, 33, 33], color="#90be6d"),
        ],
    )
