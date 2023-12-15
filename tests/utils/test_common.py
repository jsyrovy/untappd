import mock

from utils.common import (
    get_random_user_agent,
    USER_AGENTS,
    download_page,
    get_template,
    random_sleep,
    get_profile_url,
    is_test,
)


def test_get_random_user_agent():
    assert get_random_user_agent() in USER_AGENTS


def test_download_page():
    with mock.patch("utils.common.requests.get") as get_mock:
        type(get_mock.return_value).text = mock.PropertyMock(return_value="hi")
        assert download_page("") == "hi"


def test_get_template():
    name = "pivni-valka.html"
    assert get_template(name).name == name


def test_random_sleep():
    with mock.patch("utils.common.time.sleep") as sleep_mock:
        random_sleep()
        sleep_mock.assert_called_once()


def test_get_profile_url():
    assert get_profile_url("Peter") == "https://untappd.com/user/Peter"


def test_is_test():
    assert is_test()
