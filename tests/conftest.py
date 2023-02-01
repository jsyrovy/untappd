import pytest

from database import db


@pytest.fixture(scope="function", autouse=True)
def use_fresh_test_db():
    db.__init__(use_test_db=True)
    yield
