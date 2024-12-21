import pytest

from database.models import Archive, PivniValka
from database.orm import engine
from database.utils import load_dump


@pytest.fixture(scope="function", autouse=True)
def use_fresh_test_db():
    PivniValka.__table__.drop(engine)
    Archive.__table__.drop(engine)
    load_dump(engine, use_test_db=True)
