import random
import time

import utils


def main():
    user_profile_jirka = utils.download_user_profile('sejrik')
    unique_beers_count_jirka = utils.parse_unique_beers_count(user_profile_jirka)

    time.sleep(random.randrange(5))

    user_profile_dan = utils.download_user_profile('mencik2')
    unique_beers_count_dan = utils.parse_unique_beers_count(user_profile_dan)

    utils.save_stats(unique_beers_count_jirka, unique_beers_count_dan)
    utils.publish_page('pivni-valka/index.html', unique_beers_count_jirka, unique_beers_count_dan)

    print(f'{unique_beers_count_jirka=}\n{unique_beers_count_dan=}')


if __name__ == '__main__':
    main()
