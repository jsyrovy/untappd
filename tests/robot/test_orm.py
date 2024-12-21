from unittest import mock

import pytest

from robot.orm import OrmRobot


def test_orm_robot():
    robot = OrmRobot()
    with pytest.raises(NotImplementedError):
        robot.run()


def test_orm_robot_dump():
    robot = OrmRobot()
    with mock.patch("robot.orm.dump") as dump_mock, mock.patch.object(robot, "_main") as main_mock:
        robot.run()

    main_mock.assert_called_once()
    dump_mock.assert_called_once()
