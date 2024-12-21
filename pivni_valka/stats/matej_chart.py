import utils.user
from pivni_valka.stats.common import ChartData, ChartDataset
from pivni_valka.stats.total_chart import _get_chart_labels, _get_user_data


def get_chart_data(days: int) -> ChartData:
    datasets = [
        ChartDataset(user.name, _get_user_data(user.user_name, days), user.color)
        for user in utils.user.USERS
        if user.user_name in ("Mates511", "sejrik", "mencik2")
    ]

    dataset_jirka = datasets[0]
    dataset_dan = datasets[1]
    dataset_matej = datasets[2]

    for i, value in enumerate(dataset_matej.data):
        dataset_jirka.data[i] -= value
        dataset_dan.data[i] -= value

    return ChartData(_get_chart_labels(days), [dataset_jirka, dataset_dan])
