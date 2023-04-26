from sqlalchemy import create_engine

from utils import ENCODING, is_test

DUMP_PATH = "data/data_dump.sql"
TEST_DUMP_PATH = "data/test_dump.sql"

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


def load_dump(use_test_db: bool = False) -> None:
    with open(
        TEST_DUMP_PATH if use_test_db else DUMP_PATH, "r", encoding=ENCODING
    ) as f:
        with engine.connect() as conn:
            conn.connection.executescript(f.read())  # type: ignore[attr-defined]
    print("Dump loaded.")


def dump(path: str = "") -> None:
    with open(path or DUMP_PATH, "w", encoding=ENCODING) as f:
        with engine.connect() as conn:
            for line in conn.connection.iterdump():  # type: ignore[attr-defined]
                f.write(f"{line}\n")
    print("Dump created.")


load_dump(is_test())
