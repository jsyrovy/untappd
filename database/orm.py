from sqlalchemy import create_engine

from database.database import DUMP_PATH, TEST_DUMP_PATH
from utils import ENCODING, is_test

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


def load_dump(use_test_db: bool = False) -> None:
    with open(
        TEST_DUMP_PATH if use_test_db else DUMP_PATH, "r", encoding=ENCODING
    ) as f:
        with engine.connect() as conn:
            conn.connection.executescript(f.read())  # type: ignore[attr-defined]
    print("Dump loaded.")


def dump() -> None:
    with open(DUMP_PATH, "w", encoding=ENCODING) as f:
        with engine.connect() as conn:
            for line in conn.connection.iterdump():  # type: ignore[attr-defined]
                f.write(f"{line}\n")
    print("Dump created.")


load_dump(is_test())
