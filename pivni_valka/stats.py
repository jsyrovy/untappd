from pathlib import Path
from pprint import pprint

import csv_to_sqlite

import utils

CSV_PATH = 'pivni_valka/stats.csv'
DAILY_STATS_PATH = 'pivni_valka/daily_stats.csv'

TABLE = 'daily_stats'

DAILY = 'daily'
WEEKLY = 'weekly'
MONTHLY = 'monthly'


def main() -> None:
    create_db_from_csv(recreate=True)
    utils.db.dump()

    maxima = get_maxima()
    pprint(maxima)


def create_db_from_csv(recreate: bool = False) -> None:
    csv_path = Path(DAILY_STATS_PATH)
    db_path = Path(utils.db.PATH)

    if not recreate and db_path.exists() and csv_path.stat().st_mtime < db_path.stat().st_mtime:
        return
    elif db_path.exists():
        db_path.unlink()

    options = csv_to_sqlite.CsvOptions(encoding=utils.ENCODING)
    csv_to_sqlite.write_csv([str(csv_path)], str(db_path), options)


def get_maxima() -> dict[str, dict[str, tuple[str, int]]]:
    stats = {}

    for user in utils.user.USER_NAMES:
        user_stats = {}

        res = utils.db.cur.execute(f'SELECT date, max(`{user}`) FROM `{TABLE}`')
        user_stats[DAILY] = res.fetchone()

        res = utils.db.cur.execute(
            f'''SELECT strftime('%Y-%W', date) as week, sum(`{user}`) as sum
            FROM `{TABLE}` GROUP BY week ORDER BY sum DESC, week LIMIT 1'''
        )
        user_stats[WEEKLY] = res.fetchone()

        res = utils.db.cur.execute(
            f'''SELECT strftime('%Y-%m', date) as month, sum(`{user}`) as sum
            FROM `{TABLE}` GROUP BY month ORDER BY sum DESC, month LIMIT 1'''
        )
        user_stats[MONTHLY] = res.fetchone()

        stats[user] = user_stats

    return stats
