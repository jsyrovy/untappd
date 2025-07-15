import pytest

from database.models import Base
from database.orm import engine
from database.utils import load_dump


@pytest.fixture(autouse=True)
def use_fresh_test_db():
    Base.metadata.drop_all(engine)
    load_dump(engine, use_test_db=True)
