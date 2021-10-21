import argparse
import random
import time
from typing import Tuple

import pivni_valka.utils as utils


def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--local', action='store_true', help="don't download data from website")
    args = parser.parse_args()

    unique_beers_count_jirka, unique_beers_count_dan = get_unique_beers_count(args.local)

    utils.save_stats(unique_beers_count_jirka, unique_beers_count_dan)
    chart_labels, chart_data_jirka, chart_data_dan = utils.get_stats()
    utils.publish_page(
        'pivni_valka/index.html',
        unique_beers_count_jirka,
        unique_beers_count_dan,
        chart_labels,
        chart_data_jirka,
        chart_data_dan,
    )

    print(f'{unique_beers_count_jirka=}\n{unique_beers_count_dan=}')


def get_unique_beers_count(local: bool) -> Tuple[int, int]:
    if local:
        return random.randrange(1000), random.randrange(1000)

    user_profile_jirka = utils.download_user_profile('sejrik')
    unique_beers_count_jirka = utils.parse_unique_beers_count(user_profile_jirka)

    time.sleep(random.randrange(5))

    user_profile_dan = utils.download_user_profile('mencik2')
    unique_beers_count_dan = utils.parse_unique_beers_count(user_profile_dan)

    return unique_beers_count_jirka, unique_beers_count_dan
