import os

import mock
import pytest

from utils.pushover import send_notification


@pytest.fixture(scope="function", name="os_environ")
def fixture_os_environ():
    return mock.patch.dict(os.environ, {"PUSHOVER_TOKEN": "token", "PUSHOVER_USER_KEY": "key"})


def test_send_notification(os_environ):
    with os_environ, mock.patch("utils.common.requests.post") as post_mock:
        send_notification("test")

    post_mock.assert_called_once()
