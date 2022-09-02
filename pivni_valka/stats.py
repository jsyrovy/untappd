import datetime

import utils

CSV_PATH = 'pivni_valka/stats.csv'
DAILY_STATS_PATH = 'pivni_valka/daily_stats.csv'


def save_daily_stats(date: datetime.date, user_name: str, count: int):
    utils.db.cur.execute('SELECT 1 FROM pivni_valka WHERE `date` = ? and user = ?', (date, user_name))
    exists = utils.db.cur.fetchone()

    if exists:
        utils.db.cur.execute(
            'UPDATE pivni_valka SET unique_beers = ? WHERE `date` = ? and user = ?',
            (count, date, user_name),
        )
    else:
        utils.db.cur.execute(
            'INSERT INTO pivni_valka (`date`, user, unique_beers) VALUES (?, ?, ?)',
            (date, user_name, count)
        )

    utils.db.con.commit()
