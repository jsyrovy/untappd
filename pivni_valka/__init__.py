import datetime
import logging
import pathlib
import random
from collections import OrderedDict
from typing import List, Tuple, Optional

import jinja2
from bs4 import BeautifulSoup

import utils

STATS_PATH = 'pivni_valka/stats.csv'


def run() -> None:
    unique_beers_count_jirka, unique_beers_count_dan, unique_beers_count_matej = get_unique_beers_count(
        utils.is_run_locally()
    )

    save_stats(unique_beers_count_jirka, unique_beers_count_dan, unique_beers_count_matej)
    chart_labels, chart_data_jirka, chart_data_dan, chart_data_matej = get_stats(days=14)
    diff_jirka = get_diff(chart_data_jirka)
    diff_dan = get_diff(chart_data_dan)
    diff_matej = get_diff(chart_data_matej)
    page = get_page(
        utils.get_template('pivni-valka.html'),
        unique_beers_count_jirka=unique_beers_count_jirka,
        unique_beers_count_dan=unique_beers_count_dan,
        unique_beers_count_matej=unique_beers_count_matej,
        chart_labels=chart_labels,
        chart_data_jirka=chart_data_jirka,
        chart_data_dan=chart_data_dan,
        chart_data_matej=chart_data_matej,
        diff_jirka=get_formatted_diff(diff_jirka),
        diff_dan=get_formatted_diff(diff_dan),
        diff_matej=get_formatted_diff(diff_matej),
    )

    with open('pivni_valka/index.html', 'w', encoding=utils.ENCODING) as f:
        f.write(page)

    chart_labels, chart_data_jirka, chart_data_dan, chart_data_matej = get_stats(days=365)
    page_year = get_page(
        utils.get_template('pivni-valka-chart.html'),
        chart_labels=chart_labels,
        chart_data_jirka=chart_data_jirka,
        chart_data_dan=chart_data_dan,
        chart_data_matej=chart_data_matej,
    )

    with open('pivni_valka/chart_year.html', 'w', encoding=utils.ENCODING) as f:
        f.write(page_year)

    chart_labels, chart_data_jirka, chart_data_dan, chart_data_matej = get_stats()
    page_all = get_page(
        utils.get_template('pivni-valka-chart.html'),
        chart_labels=chart_labels,
        chart_data_jirka=chart_data_jirka,
        chart_data_dan=chart_data_dan,
        chart_data_matej=chart_data_matej,
    )

    with open('pivni_valka/chart_all.html', 'w', encoding=utils.ENCODING) as f:
        f.write(page_all)

    if not utils.is_run_locally() and diff_jirka + diff_dan + diff_matej > 0:
        twitter_client = utils.twitter.Client()
        status = get_tweet_status(
            unique_beers_count_jirka, unique_beers_count_dan, unique_beers_count_matej, diff_jirka, diff_dan, diff_matej
        )

        try:
            twitter_client.tweet(status)
        except utils.twitter.DuplicateTweetError:
            logging.warning(f'Tweet jiz existuje: {status}')

    logging.info(f'{unique_beers_count_jirka=} {unique_beers_count_dan=} {unique_beers_count_matej=}')


def get_unique_beers_count(local: bool) -> Tuple[int, int, int]:
    if local:
        return random.randrange(1000), random.randrange(1000), random.randrange(1000)

    user_profile_jirka = download_user_profile('sejrik')
    unique_beers_count_jirka = parse_unique_beers_count(user_profile_jirka)

    utils.random_sleep()

    user_profile_dan = download_user_profile('mencik2')
    unique_beers_count_dan = parse_unique_beers_count(user_profile_dan)

    utils.random_sleep()

    user_profile_matej = download_user_profile('Mates511')
    unique_beers_count_matej = parse_unique_beers_count(user_profile_matej)

    return unique_beers_count_jirka, unique_beers_count_dan, unique_beers_count_matej


def download_user_profile(user_name: str) -> str:
    return utils.download_page(f'{utils.BASE_URL}/user/{user_name}')


def parse_unique_beers_count(user_profile: str) -> int:
    soup = BeautifulSoup(user_profile, 'html.parser')

    try:
        unique_beers_count = soup.find('div', class_='stats').find_all('a')[1].find('span', class_='stat').text
    except Exception as e:
        raise ValueError('Cannot parse user profile.') from e

    return int(unique_beers_count.replace(',', ''))


def get_stats(days: Optional[int] = None) -> Tuple[List[str], List[int], List[int], List[int]]:
    data = OrderedDict()
    chart_labels = []
    chart_data_jirka = []
    chart_data_dan = []
    chart_data_matej = []

    with open(STATS_PATH, 'r', encoding=utils.ENCODING) as f:
        for line in f.readlines()[1:]:
            date, unique_beers_count_jirka, unique_beers_count_dan, unique_beers_count_matej = line.split(',')
            data[date] = {
                'unique_beers_count_jirka': int(unique_beers_count_jirka),
                'unique_beers_count_dan': int(unique_beers_count_dan),
                'unique_beers_count_matej': int(unique_beers_count_matej),
            }

    for key in data:
        chart_labels.append(key)
        chart_data_jirka.append(data[key]['unique_beers_count_jirka'])
        chart_data_dan.append(data[key]['unique_beers_count_dan'])
        chart_data_matej.append(data[key]['unique_beers_count_matej'])

    if not days:
        return chart_labels, chart_data_jirka, chart_data_dan, chart_data_matej

    return chart_labels[-days:], chart_data_jirka[-days:], chart_data_dan[-days:], chart_data_matej[-days:]


def get_diff(chart_data: List[int]) -> int:
    try:
        return chart_data[-1] - chart_data[-2]
    except IndexError:
        return 0


def get_formatted_diff(diff: int) -> str:
    return f'+{diff}' if diff > 0 else str(diff)


def get_page(template: jinja2.Template, **kwargs) -> str:
    return template.render(**kwargs)


def save_stats(unique_beers_count_jirka: int, unique_beers_count_dan: int, unique_beers_count_matej: int) -> None:
    path = pathlib.Path(STATS_PATH)

    lines = [
        f'{datetime.date.today()},{unique_beers_count_jirka},{unique_beers_count_dan},{unique_beers_count_matej}\n'
    ]

    if not path.exists():
        lines.insert(0, 'date,jirka,dan,matej\n')

    with path.open('a', encoding=utils.ENCODING) as f:
        f.writelines(lines)


def get_tweet_status(
    unique_beers_count_jirka: int,
    unique_beers_count_dan: int,
    unique_beers_count_matej: int,
    diff_jirka: int,
    diff_dan: int,
    diff_matej: int,
) -> str:
    status = ''

    if diff_jirka == diff_dan == diff_matej == 0:
        return status

    if diff_jirka > 0:
        status += f'Jirka včera vypil {diff_jirka} 🍺.'

    if diff_dan > 0:
        status += f'{" " if status else ""}Dan včera vypil {diff_dan} 🍺.'

    if diff_matej > 0:
        status += f'{" " if status else ""}Matěj včera vypil {diff_matej} 🍺.'

    status += (
        f' Jirka má celkem {unique_beers_count_jirka} 🍺, '
        f'Dan {unique_beers_count_dan} 🍺 a '
        f'Matěj {unique_beers_count_matej} 🍺.'
    )

    return status
