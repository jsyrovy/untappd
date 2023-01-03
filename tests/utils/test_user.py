import pytest

from utils.user import get, UserNotFound


def test_get():
    user = get("sejrik")
    assert user.user_name == "sejrik"


def test_get_with_error():
    with pytest.raises(UserNotFound):
        get("lol")
