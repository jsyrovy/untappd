import argparse
import random

import jinja2 as jinja2
import requests

USER_AGENTS = (
    'Windows 10/ Edge browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'Windows 7/ Chrome browser:  Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Mac OS X10/Safari browser: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Linux PC/Firefox browser: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Chrome OS/Chrome browser: Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
)
BASE_URL = 'https://untappd.com'


def is_run_locally():
    parser = argparse.ArgumentParser()
    parser.add_argument('--local', action='store_true', help="don't download data from website")
    return parser.parse_args().local


def get_random_user_agent() -> str:
    return random.choice(USER_AGENTS)


def download_page(url: str) -> str:
    headers = {'User-Agent': get_random_user_agent()}

    r = requests.get(url, headers=headers)

    return r.text


def get_template(file: str) -> jinja2.Template:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates'),
        autoescape=jinja2.select_autoescape(["html", "xml"]),
    )
    return env.get_template(file)
