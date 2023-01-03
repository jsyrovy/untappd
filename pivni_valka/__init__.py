import datetime
import logging
import random

import jinja2
from bs4 import BeautifulSoup

import utils
from pivni_valka.stats import common, tiles, total_chart, weekly_chart, matej_chart
from robot.db import DbRobot


class PivniValka(DbRobot):
    def _main(self) -> None:
        unique_beers_count = self.get_unique_beers_count()
        users_with_new_beers = self.save_daily_stats_db(unique_beers_count)
        page = self.get_page(
            utils.get_template("pivni-valka.html"),
            tiles_data=tiles.get_tiles_data(),
            total_chart_data=total_chart.get_chart_data(days=14),
            weekly_chart_data=weekly_chart.get_chart_data(),
            matej_chart_data=matej_chart.get_chart_data(days=90),
            grid_template_areas=self.get_grid_template_areas(),
            mobile_grid_template_areas=self.get_mobile_grid_template_areas(),
        )

        with open("web/pivni_valka/index.html", "w", encoding=utils.ENCODING) as f:
            f.write(page)

        page_month = self.get_page(
            utils.get_template("pivni-valka-chart.html"),
            total_chart_data=total_chart.get_chart_data(days=30),
            link="chart_year.html",
        )

        with open("web/pivni_valka/chart_month.html", "w", encoding=utils.ENCODING) as f:
            f.write(page_month)

        page_year = self.get_page(
            utils.get_template("pivni-valka-chart.html"),
            total_chart_data=total_chart.get_chart_data(days=365),
            link="chart_all.html",
        )

        with open("web/pivni_valka/chart_year.html", "w", encoding=utils.ENCODING) as f:
            f.write(page_year)

        page_all = self.get_page(
            utils.get_template("pivni-valka-chart.html"),
            total_chart_data=total_chart.get_chart_data(),
        )

        with open("web/pivni_valka/chart_all.html", "w", encoding=utils.ENCODING) as f:
            f.write(page_all)

        if not self._args.local and not self._args.tweetless and users_with_new_beers:
            twitter_client = utils.twitter.Client()
            status = self.get_tweet_status(users_with_new_beers)

            try:
                twitter_client.tweet(status)
            except utils.twitter.DuplicateTweetError:
                logging.warning(f"Tweet jiz existuje: {status}")

    def get_unique_beers_count(self) -> dict[str, int]:
        data: dict[str, int] = {}

        if self._args.publish:
            return data

        if self._args.local:
            total_unique_beers = common.get_total_unique_beers()
            for user_name in utils.user.USER_NAMES:
                data[user_name] = total_unique_beers[user_name] + random.randint(0, 10)
            return data

        for user_name in utils.user.USER_NAMES:
            user_profile = utils.download_page(utils.get_profile_url(user_name))
            data[user_name] = self.parse_unique_beers_count(user_profile)
            utils.random_sleep()

        return data

    def parse_unique_beers_count(self, user_profile: str) -> int:
        soup = BeautifulSoup(user_profile, "html.parser")

        try:
            unique_beers_count = (
                soup.find("div", class_="stats")
                .find_all("a")[1]
                .find("span", class_="stat")
                .text
            )
        except Exception as e:
            raise ValueError("Cannot parse user profile.") from e

        return int(unique_beers_count.replace(",", ""))

    def get_page(self, template: jinja2.Template, **kwargs) -> str:
        return template.render(**kwargs)

    def save_daily_stats_db(self, unique_beers_count: dict[str, int]) -> list[str]:
        users_with_new_beers: list[str] = []

        if not unique_beers_count:
            return users_with_new_beers

        yesterday = datetime.date.today() - datetime.timedelta(days=1)

        for user_name in utils.user.USER_NAMES:
            new_beers = unique_beers_count[user_name] - common.get_unique_beers_before(
                user_name, before=yesterday
            )
            common.save_daily_stats(yesterday, user_name, new_beers)

            if new_beers:
                users_with_new_beers.append(user_name)

        return users_with_new_beers

    def get_tweet_status(self, users_with_new_beers: list[str]) -> str:
        if not users_with_new_beers:
            return ""

        total_unique_beers = common.get_total_unique_beers()

        values = [
            f"{user.name} včera vypil {common.get_unique_beers(user.user_name, days=1)} 🍺."
            for user in utils.user.VISIBLE_USERS
            if user.user_name in users_with_new_beers
        ]
        values.extend(
            f"{user.name} má celkem {total_unique_beers[user.user_name]} 🍺."
            for user in utils.user.VISIBLE_USERS
        )

        return " ".join(values)

    def get_grid_template_areas(self) -> tuple[str, ...]:
        user_items = [f"item-{user_name}" for user_name in utils.user.VISIBLE_USER_NAMES]

        return (
            f'"{" ".join([item for item in user_items])}"',
            f'"{" ".join(["item-total-chart"] * len(user_items))}"',
            f'"{" ".join(["item-weekly-chart"] * len(user_items))}"',
            f'"{" ".join(["item-matej-chart"] * len(user_items))}"',
            f'"{" ".join(["item-twitter"] * len(user_items))}"',
        )

    def get_mobile_grid_template_areas(self) -> list[str]:
        user_items = [f'"item-{user_name}"' for user_name in utils.user.VISIBLE_USER_NAMES]
        user_items.extend(
            [
                '"item-total-chart"',
                '"item-weekly-chart"',
                '"item-matej-chart"',
                '"item-twitter"',
            ]
        )

        return user_items
