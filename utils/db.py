import sqlite3

from .common import ENCODING

PATH = 'data.sqlite'
DUMP_PATH = 'data_dump.sql'


class Db:
    def __init__(self) -> None:
        self.con = sqlite3.connect(PATH)
        self.cur = self.con.cursor()

    def dump(self) -> None:
        with open(DUMP_PATH, 'w', encoding=ENCODING) as f:
            for line in self.con.iterdump():
                f.write(f'{line}\n')

    def close(self) -> None:
        self.con.close()
