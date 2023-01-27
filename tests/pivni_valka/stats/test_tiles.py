from db import use_fresh_test_db
from pivni_valka.stats.tiles import get_tiles_data, TileData


@use_fresh_test_db
def test_get_tiles_data():
    assert get_tiles_data() == [
        TileData(
            name='Jirka',
            user_name='sejrik',
            url='https://untappd.com/user/sejrik',
            color='#577590',
            unique_beers_count=11,
            diff_day='+10',
            diff_week='+11',
            diff_month='+11',
            has_crown=True,
        ),
        TileData(
            name='Dan',
            user_name='mencik2',
            url='https://untappd.com/user/mencik2',
            color='#43aa8b',
            unique_beers_count=22,
            diff_day='+20',
            diff_week='+22',
            diff_month='+22',
            has_crown=False,
        ),
        TileData(
            name='Matěj',
            user_name='Mates511',
            url='https://untappd.com/user/Mates511',
            color='#90be6d',
            unique_beers_count=33,
            diff_day='+30',
            diff_week='+33',
            diff_month='+33',
            has_crown=False,
        ),
    ]
