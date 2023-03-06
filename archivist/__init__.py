import datetime
import os
import re
import time
from dataclasses import dataclass
from typing import Optional

import feedparser

from database.auto_init import db
from robot.db import DbRobot


@dataclass
class Record:
    id: int
    dt_utc: datetime.datetime
    user: str
    beer: str
    brewery: str
    venue: Optional[str]


class Archivist(DbRobot):
    def _main(self) -> None:
        user = "sejrik"
        key = os.environ["FEED_KEY"]
        records = []
        feed = feedparser.parse(f"https://untappd.com/rss/user/{user}?key={key}")

        for entry in feed.entries:
            records.append(
                Record(
                    get_id(entry.id),
                    get_dt(entry.published_parsed),
                    user,
                    get_beer(entry.title),
                    get_brewery(entry.title),
                    get_venue(entry.title),
                )
            )

        for record in records:
            if not is_record_in_db(record):
                print(f"Saved to DB: {record}")
                create_record_in_db(record)


def get_id(url: str) -> int:
    return int(url.split("/")[-1])


def get_dt(struct: time.struct_time) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(time.mktime(struct))


def get_regex_group(regex: str, text: str) -> str:
    if match := re.search(regex, text, re.IGNORECASE):
        return match.group(1).strip()

    raise ValueError(f"Regex `{regex}` not found in `{text}`.")


def get_optional_regex_group(regex: str, text: str) -> Optional[str]:
    try:
        return get_regex_group(regex, text)
    except ValueError:
        return None


def get_beer(text: str) -> str:
    return get_regex_group(r"is drinking an? (.*) by ", text)


def get_brewery(text: str) -> str:
    if "Untappd at Home" in text:
        text = text.replace("Untappd at Home", "")

    regex = r" by (.*)"
    at = " at "

    if at in text:
        regex += at

    return get_regex_group(regex, text)


def get_venue(text: str) -> Optional[str]:
    return get_optional_regex_group(r" at (.*)", text)


def is_record_in_db(record: Record) -> bool:
    return bool(db.query_one("SELECT 1 FROM `archive` WHERE `id` = ?;", (record.id,)))


def create_record_in_db(record: Record) -> None:
    db.execute(
        "INSERT INTO `archive` (`id`, `dt_utc`, `user`, `beer`, `brewery`, `venue`) VALUES (?, ?, ?, ?, ?, ?);",
        (
            record.id,
            record.dt_utc,
            record.user,
            record.beer,
            record.brewery,
            record.venue,
        ),
    )
