from sqlite3 import ProgrammingError

import mock
import pytest

from db import db, use_fresh_test_db
from robot.db import DbRobot


@use_fresh_test_db
def test_db_robot():
    robot = DbRobot()
    robot._main = mock.Mock()
    with mock.patch.object(db, "dump") as dump_mock:
        with mock.patch.object(db, "close") as close_mock:
            robot.run()
            dump_mock.assert_called_once()
            close_mock.assert_called_once()


@use_fresh_test_db
def test_base_robot_with_error():
    robot = DbRobot()
    with pytest.raises(NotImplementedError):
        robot.run()


@use_fresh_test_db
def test_dump():
    with mock.patch("builtins.open", mock.mock_open()) as dump_mock:
        db.dump()
        dump_mock.assert_called_once_with("data/data_dump.sql", "w", encoding="utf-8")


@use_fresh_test_db
def test_close():
    db.close()
    with pytest.raises(ProgrammingError):
        db.con.execute("select 1")


@use_fresh_test_db
def test_commit():
    db.execute("BEGIN;")
    db.execute("INSERT INTO pivni_valka VALUES('2023-01-01','Pickles',666);")
    assert db.con.in_transaction
    db.commit()
    assert not db.con.in_transaction
