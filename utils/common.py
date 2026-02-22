import random
import sys
import time

import httpx
import jinja2

ENCODING = "utf-8"
USER_AGENTS = (
    "Windows 10/ Edge browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",  # noqa: E501
    "Windows 7/ Chrome browser:  Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",  # noqa: E501
    "Mac OS X10/Safari browser: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",  # noqa: E501
    "Linux PC/Firefox browser: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    "Chrome OS/Chrome browser: Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",  # noqa: E501
)
BASE_URL = "https://untappd.com"
TIMEOUT = 5  # seconds


def get_random_user_agent() -> str:
    return random.choice(USER_AGENTS)


def download_page(url: str) -> str:
    headers = {"User-Agent": get_random_user_agent()}

    with httpx.Client(http2=True, headers=headers) as client:
        r = client.get(url)

    r.raise_for_status()
    return r.text


def get_template(file: str, templates_paths: tuple[str, ...] = ("templates",)) -> jinja2.Template:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates_paths),
        autoescape=jinja2.select_autoescape(["html", "xml"]),
    )
    return env.get_template(file)


def random_sleep(max_: int = 5) -> None:
    time.sleep(random.randrange(max_))


def get_profile_url(user_name: str) -> str:
    return f"{BASE_URL}/user/{user_name}"


def is_test() -> bool:
    return "pytest" in sys.modules
