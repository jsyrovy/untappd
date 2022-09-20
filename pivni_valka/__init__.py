import datetime
import logging
import random
from dataclasses import dataclass

import jinja2
from bs4 import BeautifulSoup

import utils
from pivni_valka import stats


@dataclass
class User:
    name: str
    profile: str
    unique_beers_count: int = 0
    drank: bool = False

    @property
    def url(self) -> str:
        return f'{utils.BASE_URL}/user/{self.profile}'


def run() -> None:
    users = (
        User('Jirka', 'sejrik'),
        User('Dan', 'mencik2'),
        User('Matěj', 'Mates511'),
        User('Ondra', 'ominar'),
    )

    local, tweetless = utils.get_run_args()
    set_unique_beers_count(users, local)
    save_daily_stats_db(users)
    utils.db.dump()
    page = get_page(
        utils.get_template('pivni-valka.html'),
        tiles_data=stats.get_tiles_data(),
        chart_data=stats.get_chart_data(days=14),
        grid_template_areas=get_grid_template_areas(users),
        mobile_grid_template_areas=get_mobile_grid_template_areas(users),
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

    if not local and not tweetless and any([user.drank for user in users]):
        twitter_client = utils.twitter.Client()
        status = get_tweet_status(users)

        try:
            twitter_client.tweet(status)
        except utils.twitter.DuplicateTweetError:
            logging.warning(f'Tweet jiz existuje: {status}')

    logging.info(users)


def set_unique_beers_count(users: tuple[User, ...], local: bool) -> None:
    if local:
        total_unique_beers = stats.get_total_unique_beers()
        for user in users:
            user.unique_beers_count = total_unique_beers[user.profile] + random.randint(0, 10)
        return

    for user in users:
        user_profile = utils.download_page(user.url)
        user.unique_beers_count = parse_unique_beers_count(user_profile)
        utils.random_sleep()


def parse_unique_beers_count(user_profile: str) -> int:
    soup = BeautifulSoup(user_profile, 'html.parser')

    try:
        unique_beers_count = soup.find('div', class_='stats').find_all('a')[1].find('span', class_='stat').text
    except Exception as e:
        raise ValueError('Cannot parse user profile.') from e

    return int(unique_beers_count.replace(',', ''))


def get_page(template: jinja2.Template, **kwargs) -> str:
    return template.render(**kwargs)


def save_daily_stats_db(users: tuple[User, ...]) -> None:
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    for user in users:
        new_beers = user.unique_beers_count - stats.get_unique_beers_before(user.profile, before=yesterday)
        stats.save_daily_stats(yesterday, user.profile, new_beers)
        user.drank = new_beers > 0


def get_tweet_status(users: tuple[User, ...]) -> str:
    if not any([user.drank for user in users]):
        return ''

    values = [
        f'{user.name} včera vypil {stats.get_unique_beers(user.profile, days=1)} 🍺.'
        for user in users if stats.get_unique_beers(user.profile, days=1)
    ]
    values.extend(f'{user.name} má celkem {user.unique_beers_count} 🍺.' for user in users)

    return ' '.join(values)


def get_grid_template_areas(users: tuple[User, ...]) -> tuple[str, str, str]:
    user_items = [f'item-{user.profile}' for user in users]

    return (
        f'"{" ".join([item for item in user_items])}"',
        f'"{" ".join(["item-chart"] * len(user_items))}"',
        f'"{" ".join(["item-twitter"] * len(user_items))}"',
    )


def get_mobile_grid_template_areas(users: tuple[User, ...]) -> list[str]:
    user_items = [f'"item-{user.profile}"' for user in users]
    user_items.extend(['"item-chart"', '"item-twitter"'])

    return user_items
