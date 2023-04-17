import requests
import os


def send_notification(text: str) -> None:
    r = requests.post(
        "https://api.pushover.net:443/1/messages.json",
        json={
            "token": os.environ["PUSHOVER_TOKEN"],
            "user": os.environ["PUSHOVER_USER_KEY"],
            "message": text,
        },
    )

    r.raise_for_status()
