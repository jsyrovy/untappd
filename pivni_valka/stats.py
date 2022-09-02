import sqlite3
from pathlib import Path
from pprint import pprint

import csv_to_sqlite

import utils

CSV_PATH = 'pivni_valka/stats.csv'
DAILY_STATS_PATH = 'pivni_valka/daily_stats.csv'
DB_PATH = 'pivni_valka/stats.sqlite'
DUMP_PATH = 'pivni_valka/stats.sql'

TABLE = 'daily_stats'

DAILY = 'daily'
WEEKLY = 'weekly'
MONTHLY = 'monthly'


def main() -> None:
    create_db_from_csv(recreate=True)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    users = get_users(cur)
    maxima = get_maxima(cur, users)
    pprint(maxima)


def create_db_from_csv(recreate: bool = False) -> None:
    csv_path = Path(DAILY_STATS_PATH)
    db_path = Path(DB_PATH)

    if not recreate and db_path.exists() and csv_path.stat().st_mtime < db_path.stat().st_mtime:
        return
    elif db_path.exists():
        db_path.unlink()

    options = csv_to_sqlite.CsvOptions(encoding=utils.ENCODING)
    csv_to_sqlite.write_csv([str(csv_path)], str(db_path), options)


def get_users(cur: sqlite3.Cursor) -> list[str]:
    res = cur.execute("SELECT name FROM pragma_table_info(?) WHERE name != 'date' ORDER BY cid", (TABLE,))
    return [r[0] for r in res.fetchall()]


def get_maxima(cur: sqlite3.Cursor, users: list[str]) -> dict[str, dict[str, tuple[str, int]]]:
    stats = {}

    for user in users:
        user_stats = {}

        res = cur.execute(f'SELECT date, max(`{user}`) FROM `{TABLE}`')
        user_stats[DAILY] = res.fetchone()

        res = cur.execute(
            f'''SELECT strftime('%Y-%W', date) as week, sum(`{user}`) as sum
            FROM `{TABLE}` GROUP BY week ORDER BY sum DESC, week LIMIT 1'''
        )
        user_stats[WEEKLY] = res.fetchone()

        res = cur.execute(
            f'''SELECT strftime('%Y-%m', date) as month, sum(`{user}`) as sum
            FROM `{TABLE}` GROUP BY month ORDER BY sum DESC, month LIMIT 1'''
        )
        user_stats[MONTHLY] = res.fetchone()

        stats[user] = user_stats

    return stats


def dump() -> None:
    con = sqlite3.connect(DB_PATH)

    with open(DUMP_PATH, 'w', encoding=utils.ENCODING) as f:
        for line in con.iterdump():
            f.write(f'{line}\n')
