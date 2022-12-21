import mock
import pytest
import tweepy

from utils.twitter import Client, DuplicateTweetError


def test_client_without_keys():
    with pytest.raises(KeyError):
        Client()


def test_tweet():
    client = Client(
        "consumer_key", "consumer_secret", "access_token_key", "access_token_secret"
    )
    with mock.patch.object(client.api, "update_status") as update_status_mock:
        client.tweet("status")
        update_status_mock.assert_called_once_with("status")


class _Forbidden(tweepy.errors.Forbidden):
    def __init__(self, text=""):
        self.text = text

    def __str__(self):
        return self.text


def test_tweet_with_duplicate_error():
    client = Client(
        "consumer_key", "consumer_secret", "access_token_key", "access_token_secret"
    )
    with mock.patch.object(
        client.api, "update_status", side_effect=_Forbidden("Status is a duplicate.")
    ):
        with pytest.raises(DuplicateTweetError):
            client.tweet("status")


def test_tweet_with_another_error():
    client = Client(
        "consumer_key", "consumer_secret", "access_token_key", "access_token_secret"
    )
    with mock.patch.object(client.api, "update_status", side_effect=_Forbidden):
        with pytest.raises(_Forbidden):
            client.tweet("status")


def test_send_message():
    client = Client(
        "consumer_key", "consumer_secret", "access_token_key", "access_token_secret"
    )
    with mock.patch.object(
        client.api, "send_direct_message"
    ) as send_direct_message_mock:
        client.send_message("text", 1)
        send_direct_message_mock.assert_called_once_with(1, "text")
