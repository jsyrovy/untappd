from utils.user import get


def test_get():
    user = get("sejrik")
    assert user.user_name == "sejrik"
