import pytest

import pivni_valka
import utils

USER_PROFILE = ''' \
<html>
  <body>
    <div class="stats">
      <a
        href="/user/test"
        class="track-click"
        data-track="profile"
        data-href=":stats/general"
      >
        <span class="stat">777</span>
        <span class="title">Total</span> </a
      ><a
        href="/user/test/beers"
        class="track-click"
        data-track="profile"
        data-href=":stats/beerhistory"
      >
        <span class="stat">{unique_beers_count}</span>
        <span class="title">Unique</span> </a
      ><a
        href="/user/test/badges"
        class="track-click"
        data-track="profile"
        data-href=":stats/badges"
      >
        <span class="stat">555</span>
        <span class="title">Badges</span> </a
      ><a
        href="/user/test/friends"
        class="track-click"
        data-track="profile"
        data-href=":stats/friends"
      >
        <span class="stat">0</span>
        <span class="title">Friends</span>
      </a>
    </div>
  </body>
</html>
'''


def test_parse_unique_beers_count():
    user_profile = USER_PROFILE.format(unique_beers_count='1,234')

    assert pivni_valka.parse_unique_beers_count(user_profile) == 1234


def test_parse_unique_beers_count_with_invalid_user_profile():
    user_profile = '<html></html>'

    with pytest.raises(ValueError) as excinfo:
        pivni_valka.parse_unique_beers_count(user_profile)

    assert str(excinfo.value) == 'Cannot parse user profile.'


def test_parse_unique_beers_count_with_invalid_count():
    user_profile = USER_PROFILE.format(unique_beers_count='NaN')

    with pytest.raises(ValueError) as excinfo:
        pivni_valka.parse_unique_beers_count(user_profile)

    assert 'invalid literal for int() with base 10' in str(excinfo.value)


@pytest.mark.parametrize(
    ('unique_beers_count_jirka', 'unique_beers_count_dan', 'has_crown_jirka', 'has_crown_dan'),
    [
        (10, 5, True, False),
        (5, 10, False, True),
        (10, 10, False, False),
    ],
)
def test_winner_badge(unique_beers_count_jirka, unique_beers_count_dan, has_crown_jirka, has_crown_dan):
    page = pivni_valka.get_page(
        utils.get_template('pivni-valka.html', ('templates', '../templates')),
        unique_beers_count_jirka=unique_beers_count_jirka,
        unique_beers_count_dan=unique_beers_count_dan,
        chart_labels=[],
        chart_data_jirka=[],
        chart_data_dan=[],
        diff_jirka='',
        diff_dan='',
    )

    assert ('Jirka 👑' in page) == has_crown_jirka
    assert ('Dan 👑' in page) == has_crown_dan


@pytest.mark.parametrize(
    ('unique_beers_count_jirka', 'unique_beers_count_dan', 'diff_jirka', 'diff_dan', 'expected_result'),
    [
        (10, 5, 0, 0, ''),
        (10, 5, 1, 0, 'Jirka včera vypil 1 🍺. Jirka vede s 10 🍺, Dan zaostává s 5 🍺.'),
        (10, 5, 0, 1, 'Dan včera vypil 1 🍺. Jirka vede s 10 🍺, Dan zaostává s 5 🍺.'),
        (5, 10, 1, 0, 'Jirka včera vypil 1 🍺. Dan vede s 10 🍺, Jirka zaostává s 5 🍺.'),
        (5, 10, 0, 1, 'Dan včera vypil 1 🍺. Dan vede s 10 🍺, Jirka zaostává s 5 🍺.'),
        (10, 10, 1, 0, 'Jirka včera vypil 1 🍺. Oba nyní mají 10 🍺.'),
        (10, 10, 0, 1, 'Dan včera vypil 1 🍺. Oba nyní mají 10 🍺.'),
        (10, 5, 2, 1, 'Jirka včera vypil 2 🍺, Dan jen 1 🍺. Jirka vede s 10 🍺, Dan zaostává s 5 🍺.'),
        (10, 5, 1, 2, 'Dan včera vypil 2 🍺, Jirka jen 1 🍺. Jirka vede s 10 🍺, Dan zaostává s 5 🍺.'),
        (5, 10, 2, 1, 'Jirka včera vypil 2 🍺, Dan jen 1 🍺. Dan vede s 10 🍺, Jirka zaostává s 5 🍺.'),
        (5, 10, 1, 2, 'Dan včera vypil 2 🍺, Jirka jen 1 🍺. Dan vede s 10 🍺, Jirka zaostává s 5 🍺.'),
        (10, 10, 2, 1, 'Jirka včera vypil 2 🍺, Dan jen 1 🍺. Oba nyní mají 10 🍺.'),
        (10, 10, 1, 2, 'Dan včera vypil 2 🍺, Jirka jen 1 🍺. Oba nyní mají 10 🍺.'),
    ],
)
def test_get_tweet_status(unique_beers_count_jirka, unique_beers_count_dan, diff_jirka, diff_dan, expected_result):
    assert pivni_valka.get_tweet_status(
        unique_beers_count_jirka,
        unique_beers_count_dan,
        diff_jirka,
        diff_dan,
    ) == expected_result
