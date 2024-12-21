from unittest import mock

from database.orm import engine
from database.utils import DUMP_PATH, dump


def test_dump():
    with mock.patch("database.utils.open", mock.mock_open()) as mocked_open:
        dump(engine)

    mocked_open.assert_called_once_with(DUMP_PATH, "w", encoding="utf-8")
    mocked_open().write.assert_called()
