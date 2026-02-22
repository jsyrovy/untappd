from __future__ import annotations

import datetime
import random
from pathlib import Path
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup

import utils.user
from pivni_valka.stats import common, tiles, weekly_chart
from pivni_valka.stats.common import ChartData
from pivni_valka.stats.tiles import TileData
from pivni_valka.stats.total_chart import get_all_chart_data, slice_chart_data
from robot.orm import OrmRobot
from utils import pushover
from utils.common import download_page, get_profile_url, get_template, random_sleep

if TYPE_CHECKING:
    import jinja2

GetPageKwArgs = list[TileData] | ChartData | tuple[str, ...] | list[str] | str


class PivniValka(OrmRobot):
    def _main(self) -> None:
        unique_beers_count = self.get_unique_beers_count()
        users_with_new_beers = self.save_daily_stats_db(unique_beers_count)

        all_chart_data = get_all_chart_data()

        page = self.get_page(
            get_template("pivni-valka.html"),
            tiles_data=tiles.get_tiles_data(),
            total_chart_data=slice_chart_data(all_chart_data, days=14),
            weekly_chart_data=weekly_chart.get_chart_data(),
            grid_template_areas=self.get_grid_template_areas(),
            mobile_grid_template_areas=self.get_mobile_grid_template_areas(),
        )

        with Path("index.html").open("w") as f:
            f.write(page)

        page_month = self.get_page(
            get_template("pivni-valka-chart.html"),
            total_chart_data=slice_chart_data(all_chart_data, days=30),
            link="chart_year.html",
        )

        with Path("web/pivni_valka/chart_month.html").open("w") as f:
            f.write(page_month)

        page_year = self.get_page(
            get_template("pivni-valka-chart.html"),
            total_chart_data=slice_chart_data(all_chart_data, days=365),
            link="chart_all.html",
        )

        with Path("web/pivni_valka/chart_year.html").open("w") as f:
            f.write(page_year)

        page_all = self.get_page(
            get_template("pivni-valka-chart.html"),
            total_chart_data=all_chart_data,
        )

        with Path("web/pivni_valka/chart_all.html").open("w") as f:
            f.write(page_all)

        if not self._args.local and not self._args.notificationless and users_with_new_beers:
            status = self.get_yesterday_status(users_with_new_beers)
            pushover.send_notification(status)

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
            user_profile = download_page(get_profile_url(user_name))
            data[user_name] = self.parse_unique_beers_count(user_profile)
            random_sleep()

        return data

    @staticmethod
    def parse_unique_beers_count(user_profile: str) -> int:
        soup = BeautifulSoup(user_profile, "html.parser")

        try:
            unique_beers_count = soup.find("div", class_="stats").find_all("a")[1].find("span", class_="stat").text  # type: ignore[union-attr]
        except Exception as e:
            raise ValueError("Cannot parse user profile.") from e

        return int(unique_beers_count.replace(",", ""))

    @staticmethod
    def get_page(template: jinja2.Template, **kwargs: GetPageKwArgs) -> str:
        return template.render(**kwargs)

    @staticmethod
    def save_daily_stats_db(unique_beers_count: dict[str, int]) -> list[str]:
        users_with_new_beers: list[str] = []

        if not unique_beers_count:
            return users_with_new_beers

        yesterday = datetime.date.today() - datetime.timedelta(days=1)

        for user_name in utils.user.USER_NAMES:
            new_beers = unique_beers_count[user_name] - common.get_unique_beers_before(user_name, before=yesterday)
            common.save_daily_stats(yesterday, user_name, new_beers)

            if new_beers:
                users_with_new_beers.append(user_name)

        return users_with_new_beers

    @staticmethod
    def get_yesterday_status(users_with_new_beers: list[str]) -> str:
        if not users_with_new_beers:
            return ""

        total_unique_beers = common.get_total_unique_beers()

        values = [
            (
                f"{user.name} včera vypil{'a' if user.sex == 'female' else ''} "
                f"{common.get_unique_beers(user.user_name, days=1)} 🍺."
            )
            for user in utils.user.VISIBLE_USERS
            if user.user_name in users_with_new_beers
        ]
        values.extend(
            f"{user.name} má celkem {total_unique_beers[user.user_name]} 🍺." for user in utils.user.VISIBLE_USERS
        )

        return " ".join(values)

    @staticmethod
    def get_grid_template_areas() -> tuple[str, ...]:
        user_items = [f"item-{user_name}" for user_name in utils.user.VISIBLE_USER_NAMES]

        return (
            f'"{" ".join(user_items)}"',
            f'"{" ".join(["item-total-chart"] * len(user_items))}"',
            f'"{" ".join(["item-weekly-chart"] * len(user_items))}"',
        )

    @staticmethod
    def get_mobile_grid_template_areas() -> list[str]:
        user_items = [f'"item-{user_name}"' for user_name in utils.user.VISIBLE_USER_NAMES]
        user_items.extend(
            [
                '"item-total-chart"',
                '"item-weekly-chart"',
            ],
        )

        return user_items
