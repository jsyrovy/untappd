import os

import httpx

from utils.common import TIMEOUT


def send_notification(text: str) -> None:
    token = os.environ.get("PUSHOVER_TOKEN")
    user_key = os.environ.get("PUSHOVER_USER_KEY")

    if not token or not user_key:
        raise OSError("PUSHOVER_TOKEN or PUSHOVER_USER_KEY is not set in environment variables.")

    r = httpx.post(
        "https://api.pushover.net:443/1/messages.json",
        json={
            "token": token,
            "user": user_key,
            "message": text,
        },
        timeout=TIMEOUT,
    )

    r.raise_for_status()
