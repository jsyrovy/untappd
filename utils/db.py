import sqlite3

from .common import ENCODING

PATH = 'data.sqlite'
DUMP_PATH = 'data_dump.sql'

con = sqlite3.connect(PATH)
cur = con.cursor()


def dump() -> None:
    with open(DUMP_PATH, 'w', encoding=ENCODING) as f:
        for line in con.iterdump():
            f.write(f'{line}\n')
