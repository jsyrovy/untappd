from sqlalchemy import Engine

from utils.common import ENCODING

DUMP_PATH = "data/data_dump.sql"
TEST_DUMP_PATH = "data/test_dump.sql"


def load_dump(engine: Engine, use_test_db: bool = False) -> None:
    with open(TEST_DUMP_PATH if use_test_db else DUMP_PATH, encoding=ENCODING) as f:
        with engine.connect() as conn:
            conn.connection.executescript(f.read())  # type: ignore[attr-defined]
    print("Dump loaded.")


def dump(engine: Engine) -> None:
    with open(DUMP_PATH, "w", encoding=ENCODING) as f:
        with engine.connect() as conn:
            for line in conn.connection.iterdump():  # type: ignore[attr-defined]
                f.write(f"{line}\n")
    print("Dump created.")
