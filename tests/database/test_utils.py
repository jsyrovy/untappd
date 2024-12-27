from unittest.mock import mock_open, patch

from database.orm import engine
from database.utils import dump


def test_dump():
    with patch("pathlib.Path.open", mock_open()) as mocked_open:
        dump(engine)

    mocked_open.assert_called_once_with("w")
    mocked_open().write.assert_called()
