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
    (
        'unique_beers_count_jirka',
        'unique_beers_count_dan',
        'unique_beers_count_matej',
        'has_crown_jirka',
        'has_crown_dan',
        'has_crown_matej',
    ),
    [
        (10, 5, 2, True, False, False),
        (5, 10, 2, False, True, False),
        (2, 5, 10, False, False, True),
        (10, 10, 10, True, True, True),
    ],
)
def test_winner_badge(
    unique_beers_count_jirka,
    unique_beers_count_dan,
    unique_beers_count_matej,
    has_crown_jirka,
    has_crown_dan,
    has_crown_matej,
):
    users = (
        pivni_valka.User('Jirka', '', '', [], unique_beers_count_jirka),
        pivni_valka.User('Dan', '', '', [], unique_beers_count_dan),
        pivni_valka.User('Matěj', '', '', [], unique_beers_count_matej),
    )
    pivni_valka.set_crown(users)

    page = pivni_valka.get_page(
        utils.get_template('pivni-valka.html', ('templates', '../templates')),
        users=users,
        chart_labels=[],
    )

    assert ('Jirka 👑' in page) == has_crown_jirka
    assert ('Dan 👑' in page) == has_crown_dan
    assert ('Matěj 👑' in page) == has_crown_matej


@pytest.mark.parametrize(
    (
        'unique_beers_count_jirka',
        'unique_beers_count_dan',
        'unique_beers_count_matej',
        'diff_jirka',
        'diff_dan',
        'diff_matej',
        'expected_result',
    ),
    [
        (10, 5, 2, 0, 0, 0, ''),
        (10, 5, 2, 1, 0, 0, 'Jirka včera vypil 1 🍺. Jirka má celkem 10 🍺. Dan má celkem 5 🍺. Matěj má celkem 2 🍺.'),
        (10, 5, 2, 0, 1, 0, 'Dan včera vypil 1 🍺. Jirka má celkem 10 🍺. Dan má celkem 5 🍺. Matěj má celkem 2 🍺.'),
        (10, 5, 2, 0, 0, 1, 'Matěj včera vypil 1 🍺. Jirka má celkem 10 🍺. Dan má celkem 5 🍺. Matěj má celkem 2 🍺.'),
        (10, 5, 2, 1, 1, 0, 'Jirka včera vypil 1 🍺. Dan včera vypil 1 🍺. Jirka má celkem 10 🍺. Dan má celkem 5 🍺. Matěj má celkem 2 🍺.'),
        (10, 5, 2, 1, 0, 1, 'Jirka včera vypil 1 🍺. Matěj včera vypil 1 🍺. Jirka má celkem 10 🍺. Dan má celkem 5 🍺. Matěj má celkem 2 🍺.'),
        (10, 5, 2, 0, 1, 1, 'Dan včera vypil 1 🍺. Matěj včera vypil 1 🍺. Jirka má celkem 10 🍺. Dan má celkem 5 🍺. Matěj má celkem 2 🍺.'),
        (10, 5, 2, 1, 1, 1, 'Jirka včera vypil 1 🍺. Dan včera vypil 1 🍺. Matěj včera vypil 1 🍺. Jirka má celkem 10 🍺. Dan má celkem 5 🍺. Matěj má celkem 2 🍺.'),
    ],
)
def test_get_tweet_status(
    unique_beers_count_jirka,
    unique_beers_count_dan,
    unique_beers_count_matej,
    diff_jirka,
    diff_dan,
    diff_matej,
    expected_result,
):
    users = (
        pivni_valka.User('Jirka', '', '', [0, diff_jirka], unique_beers_count_jirka),
        pivni_valka.User('Dan', '', '', [0, diff_dan], unique_beers_count_dan),
        pivni_valka.User('Matěj', '', '', [0, diff_matej], unique_beers_count_matej),
    )

    assert pivni_valka.get_tweet_status(users) == expected_result
