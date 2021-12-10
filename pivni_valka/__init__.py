import datetime
import logging
import pathlib
import random
import time
from collections import OrderedDict
from typing import List, Tuple

import jinja2
from bs4 import BeautifulSoup

import utils

STATS_PATH = 'pivni_valka/stats.csv'
DAYS_IN_CHART = 14


def run() -> None:
    unique_beers_count_jirka, unique_beers_count_dan = get_unique_beers_count(utils.is_run_locally())

    save_stats(unique_beers_count_jirka, unique_beers_count_dan)
    chart_labels, chart_data_jirka, chart_data_dan = get_stats()
    diff_jirka = get_diff(chart_data_jirka)
    diff_dan = get_diff(chart_data_dan)
    page = get_page(
        utils.get_template('pivni-valka.html'),
        unique_beers_count_jirka,
        unique_beers_count_dan,
        chart_labels,
        chart_data_jirka,
        chart_data_dan,
        get_formatted_diff(diff_jirka),
        get_formatted_diff(diff_dan),
    )

    with open('pivni_valka/index.html', 'w', encoding=utils.ENCODING) as f:
        f.write(page)

    if not utils.is_run_locally() and diff_jirka + diff_dan > 0:
        twitter_client = utils.twitter.Client()
        status = get_tweet_status(unique_beers_count_jirka, unique_beers_count_dan, diff_jirka, diff_dan)

        try:
            twitter_client.tweet(status)
        except utils.twitter.DuplicateTweetError:
            logging.warning(f'Tweet jiz existuje: {status}')

    logging.info(f'{unique_beers_count_jirka=} {unique_beers_count_dan=}')


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

    with open(STATS_PATH, 'r', encoding=utils.ENCODING) as f:
        for line in f.readlines()[1:]:
            date, unique_beers_count_jirka, unique_beers_count_dan = line.split(',')
            data[date] = {
                'unique_beers_count_jirka': int(unique_beers_count_jirka),
                'unique_beers_count_dan': int(unique_beers_count_dan),
            }

    for key in data:
        chart_labels.append(key)
        chart_data_jirka.append(data[key]['unique_beers_count_jirka'])
        chart_data_dan.append(data[key]['unique_beers_count_dan'])

    return chart_labels[-DAYS_IN_CHART:], chart_data_jirka[-DAYS_IN_CHART:], chart_data_dan[-DAYS_IN_CHART:]


def get_diff(chart_data: List[int]) -> int:
    try:
        return chart_data[-1] - chart_data[-2]
    except IndexError:
        return 0


def get_formatted_diff(diff: int) -> str:
    return f'+{diff}' if diff > 0 else str(diff)


def get_page(
    template: jinja2.Template,
    unique_beers_count_jirka: int,
    unique_beers_count_dan: int,
    chart_labels: List[str],
    chart_data_jirka: List[int],
    chart_data_dan: List[int],
    diff_jirka: str,
    diff_dan: str,
) -> str:
    return template.render(
        unique_beers_count_jirka=unique_beers_count_jirka,
        unique_beers_count_dan=unique_beers_count_dan,
        chart_labels=chart_labels,
        chart_data_jirka=chart_data_jirka,
        chart_data_dan=chart_data_dan,
        diff_jirka=diff_jirka,
        diff_dan=diff_dan,
    )


def save_stats(unique_beers_count_jirka: int, unique_beers_count_dan: int) -> None:
    path = pathlib.Path(STATS_PATH)

    lines = [f'{datetime.date.today()},{unique_beers_count_jirka},{unique_beers_count_dan}\n']

    if not path.exists():
        lines.insert(0, 'date,jirka,dan\n')

    with path.open('a', encoding=utils.ENCODING) as f:
        f.writelines(lines)


def get_tweet_status(unique_beers_count_jirka: int, unique_beers_count_dan: int, diff_jirka: int, diff_dan: int) -> str:
    status = ''

    if diff_jirka == diff_dan == 0:
        return status

    if diff_jirka == 0:
        status += f'Dan včera vypil {diff_dan} 🍺.'

    if diff_dan == 0:
        status += f'Jirka včera vypil {diff_jirka} 🍺.'

    if diff_jirka > diff_dan > 0:
        status += f'Jirka včera vypil {diff_jirka} 🍺, Dan jen {diff_dan} 🍺.'
    elif diff_dan > diff_jirka > 0:
        status += f'Dan včera vypil {diff_dan} 🍺, Jirka jen {diff_jirka} 🍺.'

    status += ' '

    if unique_beers_count_jirka > unique_beers_count_dan:
        status += f'Jirka vede s {unique_beers_count_jirka} 🍺, Dan zaostává s {unique_beers_count_dan} 🍺.'
    elif unique_beers_count_dan > unique_beers_count_jirka:
        status += f'Dan vede s {unique_beers_count_dan} 🍺, Jirka zaostává s {unique_beers_count_jirka} 🍺.'
    else:
        status += f'Oba nyní mají {unique_beers_count_jirka} 🍺.'

    return status
