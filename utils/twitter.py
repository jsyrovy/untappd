import os
from typing import Optional

import tweepy
import tweepy.models


class DuplicateTweetError(Exception):
    ...


class Client:
    def __init__(
        self,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
        access_token_key: Optional[str] = None,
        access_token_secret: Optional[str] = None,
    ) -> None:
        self._consumer_key = consumer_key or os.environ['CONSUMER_KEY']
        self._consumer_secret = consumer_secret or os.environ['CONSUMER_SECRET']
        self._access_token_key = access_token_key or os.environ['ACCESS_TOKEN_KEY']
        self._access_token_secret = access_token_secret or os.environ['ACCESS_TOKEN_SECRET']
        self._auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        self._auth.set_access_token(self._access_token_key, self._access_token_secret)
        self.api = tweepy.API(self._auth)

    def tweet(self, status: str) -> None:
        try:
            self.api.update_status(status)
        except tweepy.errors.Forbidden as e:
            if 'Status is a duplicate.' in str(e):
                raise DuplicateTweetError from e

            raise
