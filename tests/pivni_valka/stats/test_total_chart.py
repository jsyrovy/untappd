from pivni_valka.stats.common import ChartData, ChartDataset
from pivni_valka.stats.total_chart import get_all_chart_data, slice_chart_data


def test_get_all_chart_data():
    result = get_all_chart_data()

    assert result == ChartData(
        labels=["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04"],
        datasets=[
            ChartDataset(label="Jirka", data=[0, 1, 1, 11], color="#577590"),
            ChartDataset(label="Dan", data=[0, 2, 2, 22], color="#43aa8b"),
            ChartDataset(label="Matěj", data=[0, 3, 3, 33], color="#90be6d"),
            ChartDataset(label="Kája", data=[0, 4, 4, 44], color="#f88379"),
        ],
    )


def test_slice_chart_data():
    full_data = get_all_chart_data()

    assert slice_chart_data(full_data, 1) == ChartData(
        labels=["2022-01-04"],
        datasets=[
            ChartDataset(label="Jirka", data=[11], color="#577590"),
            ChartDataset(label="Dan", data=[22], color="#43aa8b"),
            ChartDataset(label="Matěj", data=[33], color="#90be6d"),
            ChartDataset(label="Kája", data=[44], color="#f88379"),
        ],
    )

    assert slice_chart_data(full_data, 2) == ChartData(
        labels=["2022-01-03", "2022-01-04"],
        datasets=[
            ChartDataset(label="Jirka", data=[1, 11], color="#577590"),
            ChartDataset(label="Dan", data=[2, 22], color="#43aa8b"),
            ChartDataset(label="Matěj", data=[3, 33], color="#90be6d"),
            ChartDataset(label="Kája", data=[4, 44], color="#f88379"),
        ],
    )
