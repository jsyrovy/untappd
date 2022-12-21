import mock
import pytest

from db import db
from robot.db import DbRobot


def test_db_robot():
    robot = DbRobot()
    robot._main = mock.Mock()
    with mock.patch.object(db, "dump") as dump_mock:
        with mock.patch.object(db, "close") as close_mock:
            robot.run()
            dump_mock.assert_called_once()
            close_mock.assert_called_once()


def test_base_robot_with_error():
    robot = DbRobot()
    with pytest.raises(NotImplementedError):
        robot.run()
