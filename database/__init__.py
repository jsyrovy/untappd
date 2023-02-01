import sqlite3
from collections.abc import Iterable
from typing import Optional

from utils import ENCODING, is_test

DUMP_PATH = "data/data_dump.sql"
TEST_DUMP_PATH = "data/test_dump.sql"


class Db:
    def __init__(self, use_test_db: bool = False, database: str = ":memory:") -> None:
        self.use_test_db: bool = use_test_db
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()

        if use_test_db:
            print("DB is running in test mode.")

        self.load_dump()

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

    def load_dump(self) -> None:
        with open(
            TEST_DUMP_PATH if self.use_test_db else DUMP_PATH, "r", encoding=ENCODING
        ) as f:
            self.cur.executescript(f.read())


db = Db(use_test_db=is_test())
