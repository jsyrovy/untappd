import os

import requests

from utils.common import TIMEOUT


def send_notification(text: str) -> None:
    r = requests.post(
        "https://api.pushover.net:443/1/messages.json",
        json={
            "token": os.environ["PUSHOVER_TOKEN"],
            "user": os.environ["PUSHOVER_USER_KEY"],
            "message": text,
        },
        timeout=TIMEOUT,
    )

    r.raise_for_status()
