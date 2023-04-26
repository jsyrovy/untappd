from sqlalchemy import create_engine

from database.utils import load_dump
from utils import is_test

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

load_dump(engine, is_test())
