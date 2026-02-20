from unittest import mock

from notifier import Notifier
from notifier.base import Beer


def test_notifier_main_with_new_beers():
    mock_offer = mock.MagicMock()
    mock_offer.new_beers = [Beer("New IPA", "Brewery")]

    mock_class = mock.MagicMock(return_value=mock_offer)

    with (
        mock.patch("notifier.AmbasadaOffer", mock_class),
        mock.patch("robot.orm.dump"),
    ):
        notifier = Notifier()
        notifier._args = mock.MagicMock(notificationless=False)
        notifier._main()

    mock_offer.run.assert_called_once()
    mock_offer.set_tasted.assert_called_once()
    notificationless = False
    mock_offer.send_notification.assert_called_once_with(notificationless)


def test_notifier_main_without_new_beers():
    mock_offer = mock.MagicMock()
    mock_offer.new_beers = []

    mock_class = mock.MagicMock(return_value=mock_offer)

    with (
        mock.patch("notifier.AmbasadaOffer", mock_class),
        mock.patch("robot.orm.dump"),
    ):
        notifier = Notifier()
        notifier._args = mock.MagicMock(notificationless=False)
        notifier._main()

    mock_offer.run.assert_called_once()
    mock_offer.set_tasted.assert_not_called()
    mock_offer.send_notification.assert_not_called()
