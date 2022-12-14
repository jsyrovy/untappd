import os
import sqlite3
from collections.abc import Iterable
from typing import Optional

from utils.common import ENCODING

PATH = "data.sqlite"
TEST_DB = ":memory:"
DUMP_PATH = "data_dump.sql"
TEST_DUMP_PATH = "test_dump.sql"


class Db:
    def __init__(self, is_test: bool = False) -> None:
        self.con = sqlite3.connect(TEST_DB if is_test else PATH)
        self.cur = self.con.cursor()

        if is_test:
            print("DB is running in test mode.")
            self.load_test_dump()

    def dump(self) -> None:
        with open(DUMP_PATH, "w", encoding=ENCODING) as f:
            for line in self.con.iterdump():
                f.write(f"{line}\n")

    def close(self) -> None:
        self.con.close()

    def _execute(self, sql: str, parameters) -> None:
        if parameters:
            self.cur.execute(sql, parameters)
        else:
            self.cur.execute(sql)

    def execute(self, sql: str, parameters: Optional[Iterable] = None) -> None:
        self._execute(sql, parameters)

    def query_one(self, sql: str, parameters: Optional[Iterable] = None) -> tuple:
        self.execute(sql, parameters)
        return self.cur.fetchone()

    def query_all(self, sql: str, parameters: Optional[Iterable] = None) -> list:
        self.execute(sql, parameters)
        return self.cur.fetchall()

    def commit(self) -> None:
        self.con.commit()

    def load_test_dump(self) -> None:
        with open(TEST_DUMP_PATH, "r", encoding=ENCODING) as f:
            self.cur.executescript(f.read())


db = Db(is_test=bool(os.environ.get("TEST")))
