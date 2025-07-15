import os
from unittest import mock

import pytest

from utils.pushover import send_notification


@pytest.fixture(name="os_environ")
def fixture_os_environ():
    return mock.patch.dict(os.environ, {"PUSHOVER_TOKEN": "token", "PUSHOVER_USER_KEY": "key"})


def test_send_notification(os_environ):
    with os_environ, mock.patch("httpx.post") as post_mock:
        send_notification("test")

    post_mock.assert_called_once()


def test_send_notification_without_evn_variables():
    with pytest.raises(OSError):
        send_notification("test")
