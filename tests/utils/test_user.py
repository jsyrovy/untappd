import pytest

from utils.user import UserNotFoundError, get


def test_get():
    user = get("sejrik")
    assert user.user_name == "sejrik"


def test_get_with_error():
    with pytest.raises(UserNotFoundError):
        get("lol")
