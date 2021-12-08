import os
from typing import Optional

import tweepy
import tweepy.models


class Client:
    def __init__(
        self,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
        access_token_key: Optional[str] = None,
        access_token_secret: Optional[str] = None,
    ) -> None:
        self._consumer_key = os.environ.get('CONSUMER_KEY') or consumer_key
        self._consumer_secret = os.environ.get('CONSUMER_SECRET') or consumer_secret
        self._access_token_key = os.environ.get('ACCESS_TOKEN_KEY') or access_token_key
        self._access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET') or access_token_secret
        self._auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        self._auth.set_access_token(self._access_token_key, self._access_token_secret)
        self.api = tweepy.API(self._auth)

    def tweet(self, status: str) -> None:
        self.api.update_status(status)
