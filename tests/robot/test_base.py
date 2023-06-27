import pytest

from robot.base import BaseRobot


def test_base_robot():
    robot = BaseRobot()
    with pytest.raises(NotImplementedError):
        robot.run()


def test_args():
    robot = BaseRobot()
    assert robot._args.local is False  # pylint: disable=protected-access
    assert robot._args.notificationless is False  # pylint: disable=protected-access
    assert robot._args.publish is False  # pylint: disable=protected-access
