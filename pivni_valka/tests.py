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


def test_winner_badge():
    unique_beers_count_jirka = 10
    unique_beers_count_dan = 5

    page = _get_page(unique_beers_count_jirka, unique_beers_count_dan)

    assert unique_beers_count_jirka > unique_beers_count_dan
    assert 'Jirka 👑' in page
    assert 'Dan 👑' not in page


def test_winner_badge_dan():
    unique_beers_count_jirka = 5
    unique_beers_count_dan = 10

    page = _get_page(unique_beers_count_jirka, unique_beers_count_dan)

    assert unique_beers_count_jirka < unique_beers_count_dan
    assert 'Jirka 👑' not in page
    assert 'Dan 👑' in page


def test_no_winner_badge():
    unique_beers_count_jirka = 5
    unique_beers_count_dan = 5

    page = _get_page(unique_beers_count_jirka, unique_beers_count_dan)

    assert unique_beers_count_jirka == unique_beers_count_dan
    assert 'Jirka 👑' not in page
    assert 'Dan 👑' not in page


def _get_page(unique_beers_count_jirka, unique_beers_count_dan):
    return pivni_valka.get_page(
        utils.get_template('pivni-valka.html', '../templates'),
        unique_beers_count_jirka=unique_beers_count_jirka,
        unique_beers_count_dan=unique_beers_count_dan,
        chart_labels=[],
        chart_data_jirka=[],
        chart_data_dan=[],
        diff_jirka='',
        diff_dan='',
    )
