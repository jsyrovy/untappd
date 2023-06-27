import os

import requests

import utils


def send_notification(text: str) -> None:
    r = requests.post(
        "https://api.pushover.net:443/1/messages.json",
        json={
            "token": os.environ["PUSHOVER_TOKEN"],
            "user": os.environ["PUSHOVER_USER_KEY"],
            "message": text,
        },
        timeout=utils.TIMEOUT,
    )

    r.raise_for_status()
