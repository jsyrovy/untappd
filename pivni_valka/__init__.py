import datetime
import logging
import random

import jinja2
from bs4 import BeautifulSoup

import utils
from pivni_valka import stats


def run() -> None:
    local, tweetless = utils.get_run_args()
    unique_beers_count = get_unique_beers_count(local)
    users_with_new_beers = save_daily_stats_db(unique_beers_count)
    utils.db.dump()
    page = get_page(
        utils.get_template('pivni-valka.html'),
        tiles_data=stats.get_tiles_data(),
        chart_data=stats.get_chart_data(days=14),
        grid_template_areas=get_grid_template_areas(),
        mobile_grid_template_areas=get_mobile_grid_template_areas(),
    )

    with open('pivni_valka/index.html', 'w', encoding=utils.ENCODING) as f:
        f.write(page)

    page_month = get_page(
        utils.get_template('pivni-valka-chart.html'),
        chart_data=stats.get_chart_data(days=30),
        link='chart_year.html',
    )

    with open('pivni_valka/chart_month.html', 'w', encoding=utils.ENCODING) as f:
        f.write(page_month)

    page_year = get_page(
        utils.get_template('pivni-valka-chart.html'),
        chart_data=stats.get_chart_data(days=365),
        link='chart_all.html',
    )

    with open('pivni_valka/chart_year.html', 'w', encoding=utils.ENCODING) as f:
        f.write(page_year)

    page_all = get_page(utils.get_template('pivni-valka-chart.html'), chart_data=stats.get_chart_data())

    with open('pivni_valka/chart_all.html', 'w', encoding=utils.ENCODING) as f:
        f.write(page_all)

    if not local and not tweetless and users_with_new_beers:
        twitter_client = utils.twitter.Client()
        status = get_tweet_status(users_with_new_beers)

        try:
            twitter_client.tweet(status)
        except utils.twitter.DuplicateTweetError:
            logging.warning(f'Tweet jiz existuje: {status}')


def get_unique_beers_count(local: bool) -> dict[str, int]:
    data = {}

    if local:
        total_unique_beers = stats.get_total_unique_beers()
        for user_name in utils.user.USER_NAMES:
            data[user_name] = total_unique_beers[user_name] + random.randint(0, 10)
        return data

    for user_name in utils.user.USER_NAMES:
        user_profile = utils.download_page(utils.get_profile_url(user_name))
        data[user_name] = parse_unique_beers_count(user_profile)
        utils.random_sleep()

    return data


def parse_unique_beers_count(user_profile: str) -> int:
    soup = BeautifulSoup(user_profile, 'html.parser')

    try:
        unique_beers_count = soup.find('div', class_='stats').find_all('a')[1].find('span', class_='stat').text
    except Exception as e:
        raise ValueError('Cannot parse user profile.') from e

    return int(unique_beers_count.replace(',', ''))


def get_page(template: jinja2.Template, **kwargs) -> str:
    return template.render(**kwargs)


def save_daily_stats_db(unique_beers_count: dict[str, int]) -> list[str]:
    users_with_new_beers = []
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    for user_name in utils.user.USER_NAMES:
        new_beers = unique_beers_count[user_name] - stats.get_unique_beers_before(user_name, before=yesterday)
        stats.save_daily_stats(yesterday, user_name, new_beers)
        users_with_new_beers.append(user_name)

    return users_with_new_beers


def get_tweet_status(users_with_new_beers: list[str]) -> str:
    if not users_with_new_beers:
        return ''

    total_unique_beers = stats.get_total_unique_beers()

    values = [
        f'{user.name} včera vypil {stats.get_unique_beers(user.user_name, days=1)} 🍺.'
        for user in utils.user.USERS if user.user_name in users_with_new_beers
    ]
    values.extend(f'{user_name} má celkem {total_unique_beers[user_name]} 🍺.' for user_name in utils.user.USER_NAMES)

    return ' '.join(values)


def get_grid_template_areas() -> tuple[str, str, str]:
    user_items = [f'item-{user_name}' for user_name in utils.user.USER_NAMES]

    return (
        f'"{" ".join([item for item in user_items])}"',
        f'"{" ".join(["item-chart"] * len(user_items))}"',
        f'"{" ".join(["item-twitter"] * len(user_items))}"',
    )


def get_mobile_grid_template_areas() -> list[str]:
    user_items = [f'"item-{user_name}"' for user_name in utils.user.USER_NAMES]
    user_items.extend(['"item-chart"', '"item-twitter"'])

    return user_items
