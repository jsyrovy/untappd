from sqlalchemy import create_engine

from database.database import DUMP_PATH
from utils import ENCODING

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


def load_dump() -> None:
    with open(DUMP_PATH, "r", encoding=ENCODING) as f:
        with engine.connect() as conn:
            conn.connection.executescript(f.read())


def dump() -> None:
    with open(DUMP_PATH, "w", encoding=ENCODING) as f:
        with engine.connect() as conn:
            for line in conn.connection.iterdump():
                f.write(f"{line}\n")
