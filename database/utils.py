from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy import Engine

DUMP_PATH = "data/data_dump.sql"
TEST_DUMP_PATH = "data/test_dump.sql"


def load_dump(engine: Engine, use_test_db: bool = False) -> None:
    with (
        Path(TEST_DUMP_PATH if use_test_db else DUMP_PATH).open("r") as f,
        engine.connect() as conn,
    ):
        conn.connection.executescript(f.read())
    print("Dump loaded.")


def dump(engine: Engine) -> None:
    with (
        Path(DUMP_PATH).open("w") as f,
        engine.connect() as conn,
    ):
        f.writelines(f"{line}\n" for line in conn.connection.iterdump())
    print("Dump created.")
