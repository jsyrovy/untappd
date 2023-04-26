import pytest

from database.models import PivniValka, Archive
from database.orm import engine, load_dump


@pytest.fixture(scope="function", autouse=True)
def use_fresh_test_db():
    PivniValka.__table__.drop(engine)
    Archive.__table__.drop(engine)
    load_dump(use_test_db=True)
    yield
