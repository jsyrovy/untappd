import pytest

from db import use_fresh_test_db
from pivni_valka import PivniValka

USER_PROFILE = """ \
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
"""


@use_fresh_test_db
def test_parse_unique_beers_count():
    user_profile = USER_PROFILE.format(unique_beers_count="1,234")

    assert PivniValka().parse_unique_beers_count(user_profile) == 1234


@use_fresh_test_db
def test_parse_unique_beers_count_with_invalid_user_profile():
    user_profile = "<html></html>"

    with pytest.raises(ValueError) as excinfo:
        PivniValka().parse_unique_beers_count(user_profile)

    assert str(excinfo.value) == "Cannot parse user profile."
