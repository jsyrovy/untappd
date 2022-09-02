import datetime
import logging
import pathlib
import random
from collections import OrderedDict
from dataclasses import dataclass

import jinja2
from bs4 import BeautifulSoup

import utils
from pivni_valka import stats


class Period:
    DAY: int = 1
    WEEK: int = 7
    MONTH: int = 30


@dataclass
class User:
    name: str
    profile: str
    color: str
    chart_data: list[int]
    unique_beers_count: int = 0
    has_crown: bool = False
    days_in_chart: int = 0

    @property
    def formatted_diff_day(self) -> str:
        return self._get_formatted_diff(Period.DAY)

    @property
    def formatted_diff_week(self) -> str:
        return self._get_formatted_diff(Period.WEEK)

    @property
    def formatted_diff_month(self) -> str:
        return self._get_formatted_diff(Period.MONTH)

    @property
    def url(self) -> str:
        return f'{utils.BASE_URL}/user/{self.profile}'

    def get_chart_data(self) -> list[int]:
        return self.chart_data[-self.days_in_chart:] if self.days_in_chart else self.chart_data

    def get_diff(self, period: int) -> int:
        try:
            return self.chart_data[-1] - self.chart_data[-1 - period]
        except IndexError:
            return 0

    def _get_formatted_diff(self, period: int) -> str:
        return f'+{self.get_diff(period)}' if self.get_diff(period) > 0 else str(self.get_diff(period))


def run() -> None:
    users = (
        User('Jirka', 'sejrik', '#577590', []),
        User('Dan', 'mencik2', '#43aa8b', []),
        User('Matěj', 'Mates511', '#90be6d', []),
        User('Ondra', 'ominar', '#f9c74f', []),
    )

    local, _ = utils.get_run_args()
    set_unique_beers_count(users, local)
    set_crown(users)
    save_stats(users)
    chart_labels = get_stats(users, days=14)
    save_daily_stats(users)
    save_daily_stats_db(users)
    utils.db.dump()
    page = get_page(
        utils.get_template('pivni-valka.html'),
        users=users,
        chart_labels=chart_labels,
        grid_template_areas=get_grid_template_areas(users),
        mobile_grid_template_areas=get_mobile_grid_template_areas(users),
    )

    with open('pivni_valka/index.html', 'w', encoding=utils.ENCODING) as f:
        f.write(page)

    chart_labels = get_stats(users, days=30)
    page_month = get_page(
        utils.get_template('pivni-valka-chart.html'),
        users=users,
        chart_labels=chart_labels,
        link='chart_year.html',
    )

    with open('pivni_valka/chart_month.html', 'w', encoding=utils.ENCODING) as f:
        f.write(page_month)

    chart_labels = get_stats(users, days=365)
    page_year = get_page(
        utils.get_template('pivni-valka-chart.html'),
        users=users,
        chart_labels=chart_labels,
        link='chart_all.html',
    )

    with open('pivni_valka/chart_year.html', 'w', encoding=utils.ENCODING) as f:
        f.write(page_year)

    chart_labels = get_stats(users)
    page_all = get_page(utils.get_template('pivni-valka-chart.html'), users=users, chart_labels=chart_labels)

    with open('pivni_valka/chart_all.html', 'w', encoding=utils.ENCODING) as f:
        f.write(page_all)

    local, tweetless = utils.get_run_args()

    if not local and not tweetless and sum([user.get_diff(Period.DAY) for user in users]) > 0:
        twitter_client = utils.twitter.Client()
        status = get_tweet_status(users)

        try:
            twitter_client.tweet(status)
        except utils.twitter.DuplicateTweetError:
            logging.warning(f'Tweet jiz existuje: {status}')

    logging.info(users)


def set_unique_beers_count(users: tuple[User, ...], local: bool) -> None:
    if local:
        for user in users:
            user.unique_beers_count = random.randrange(1000)
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


def get_stats(users: tuple[User, ...], days: int = 0) -> list[str]:
    data = OrderedDict()
    chart_labels = []

    for user in users:
        user.chart_data.clear()
        user.days_in_chart = days

    with open(stats.CSV_PATH, 'r', encoding=utils.ENCODING) as f:
        for line in f.readlines()[1:]:
            date = line.split(',')[0]
            values = line.split(',')[1:]
            date_values = {}

            for i, user in enumerate(users):
                date_values[user.name] = int(values[i])

            data[date] = date_values

    for key in data:
        chart_labels.append(key)

        for user in users:
            user.chart_data.append(data[key][user.name])

    if not days:
        return chart_labels

    return chart_labels[-days:]


def get_page(template: jinja2.Template, **kwargs) -> str:
    return template.render(**kwargs)


def save_stats(users: tuple[User, ...]) -> None:
    path = pathlib.Path(stats.CSV_PATH)
    lines = [f'{datetime.date.today()},{",".join([str(user.unique_beers_count) for user in users])}\n']

    if not path.exists():
        lines.insert(0, f'date,{",".join([str(user.profile) for user in users])}\n')

    with path.open('a', encoding=utils.ENCODING) as f:
        f.writelines(lines)


def save_daily_stats(users: tuple[User, ...]) -> None:
    path = pathlib.Path(stats.DAILY_STATS_PATH)
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    lines = [f'{yesterday},{",".join([str(user.get_diff(Period.DAY)) for user in users])}\n']

    if not path.exists():
        lines.insert(0, f'date,{",".join([str(user.profile) for user in users])}\n')

    with path.open('a', encoding=utils.ENCODING) as f:
        f.writelines(lines)


def save_daily_stats_db(users: tuple[User, ...]) -> None:
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    for user in users:
        stats.save_daily_stats(yesterday, user.profile, user.get_diff(Period.DAY))


def get_tweet_status(users: tuple[User, ...]) -> str:
    if sum(user.get_diff(Period.DAY) for user in users) == 0:
        return ''

    values = [f'{user.name} včera vypil {user.get_diff(Period.DAY)} 🍺.' for user in users if user.get_diff(Period.DAY)]
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


def set_crown(users: tuple[User, ...]) -> None:
    max_ = max(user.unique_beers_count for user in users)

    for user in users:
        if user.unique_beers_count == max_:
            user.has_crown = True
