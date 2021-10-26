import datetime
import pathlib
import random
import time
from collections import OrderedDict
from typing import List, Tuple

import jinja2
from bs4 import BeautifulSoup

import utils

STATS_PATH = "pivni_valka/stats.csv"


def run() -> None:
    unique_beers_count_jirka, unique_beers_count_dan = get_unique_beers_count(utils.is_run_locally())

    save_stats(unique_beers_count_jirka, unique_beers_count_dan)
    chart_labels, chart_data_jirka, chart_data_dan = get_stats()
    publish_page(
        utils.get_template('pivni-valka.html'),
        'pivni_valka/index.html',
        unique_beers_count_jirka,
        unique_beers_count_dan,
        chart_labels,
        chart_data_jirka,
        chart_data_dan,
    )

    print(f'{unique_beers_count_jirka=}\n{unique_beers_count_dan=}')


def get_unique_beers_count(local: bool) -> Tuple[int, int]:
    if local:
        return random.randrange(1000), random.randrange(1000)

    user_profile_jirka = download_user_profile('sejrik')
    unique_beers_count_jirka = parse_unique_beers_count(user_profile_jirka)

    time.sleep(random.randrange(5))

    user_profile_dan = download_user_profile('mencik2')
    unique_beers_count_dan = parse_unique_beers_count(user_profile_dan)

    return unique_beers_count_jirka, unique_beers_count_dan


def download_user_profile(user_name: str) -> str:
    return utils.download_page(f'{utils.BASE_URL}/user/{user_name}')


def parse_unique_beers_count(user_profile: str) -> int:
    soup = BeautifulSoup(user_profile, 'html.parser')

    try:
        unique_beers_count = soup.find('div', class_='stats').find_all('a')[1].find('span', class_='stat').text
    except Exception as e:
        raise ValueError('Cannot parse user profile.') from e

    return int(unique_beers_count.replace(',', ''))


def get_stats() -> Tuple[List[str], List[int], List[int]]:
    data = OrderedDict()
    chart_labels = []
    chart_data_jirka = []
    chart_data_dan = []

    for line in pathlib.Path(STATS_PATH).read_text().splitlines()[1:]:
        date, unique_beers_count_jirka, unique_beers_count_dan = line.split(',')
        data[date] = {
            'unique_beers_count_jirka': int(unique_beers_count_jirka),
            'unique_beers_count_dan': int(unique_beers_count_dan),
        }

    for key in data:
        chart_labels.append(key)
        chart_data_jirka.append(data[key]['unique_beers_count_jirka'])
        chart_data_dan.append(data[key]['unique_beers_count_dan'])

    return chart_labels[-14:], chart_data_jirka[-14:], chart_data_dan[-14:]


def publish_page(
    template: jinja2.Template,
    path: str,
    unique_beers_count_jirka: int,
    unique_beers_count_dan: int,
    chart_labels: List[str],
    chart_data_jirka: List[int],
    chart_data_dan: List[int],
) -> None:
    page = pathlib.Path(path)
    page.write_text(
        template.render(
            unique_beers_count_jirka=unique_beers_count_jirka,
            unique_beers_count_dan=unique_beers_count_dan,
            chart_labels=chart_labels,
            chart_data_jirka=chart_data_jirka,
            chart_data_dan=chart_data_dan,
        ),
        "UTF-8",
    )


def save_stats(unique_beers_count_jirka: int, unique_beers_count_dan: int) -> None:
    path = pathlib.Path(STATS_PATH)

    lines = [f'{datetime.date.today()},{unique_beers_count_jirka},{unique_beers_count_dan}\n']

    if not path.exists():
        lines.insert(0, "date,jirka,dan\n")

    with path.open("a", encoding='utf-8') as f:
        f.writelines(lines)
