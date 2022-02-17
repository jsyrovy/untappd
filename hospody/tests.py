import datetime

import hospody


def test_create_random_check_in():
    check_in = hospody.CheckIn.get_random()

    assert check_in.id
    assert check_in.dt
    assert check_in.venue_name
    assert check_in.beer_name
    assert check_in.brewery
    assert check_in.serving
    assert check_in.beer_link
    assert check_in.venue_link


def test_create_check_in_from_json():
    json_ = {
        'id': 666,
        'dt': '2000-01-01 00:00:00',
        'beer_name': 'pivo',
        'venue_name': 'U Toulavé pípy',
        'brewery': 'pivovar',
        'serving': 'cepovane',
        'beer_link': 'https://pivo.org'
    }
    check_in = hospody.CheckIn.from_json(json_)

    assert check_in.id == json_['id']
    assert check_in.dt == datetime.datetime(2000, 1, 1, 0, 0, 0)
    assert check_in.venue_name == json_['venue_name']
    assert check_in.beer_name == json_['beer_name']
    assert check_in.brewery == json_['brewery']
    assert check_in.serving == json_['serving']
    assert check_in.beer_link == json_['beer_link']


def test_check_in_to_json():
    check_in = hospody.CheckIn(
        42,
        datetime.datetime(2000, 1, 1, 0, 0, 0),
        'hospoda',
        'pivo',
        'pivovar',
        'cepovane',
        'https://pivo.org',
        'https://hospoda.org',
    )
    json_ = check_in.to_json()

    assert json_['id'] == check_in.id
    assert json_['dt'] == '2000-01-01T00:00:00'
    assert json_['venue_name'] == check_in.venue_name
    assert json_['beer_name'] == check_in.beer_name
    assert json_['brewery'] == check_in.brewery
    assert json_['serving'] == check_in.serving
    assert json_['beer_link'] == check_in.beer_link
    assert 'venue_link' not in json_


def test_check_ins_order():
    first_check_in = hospody.CheckIn.get_random()
    middle_check_in = hospody.CheckIn.get_random()
    last_check_in = hospody.CheckIn.get_random()

    check_ins = hospody.get_unique_beers_check_ins([last_check_in, first_check_in, middle_check_in])

    assert first_check_in.dt < middle_check_in.dt < last_check_in.dt
    assert len(check_ins) == 1
    assert check_ins[0] == last_check_in


def test_check_ins_sort():
    first_check_in = hospody.CheckIn.get_random()
    middle_check_in = hospody.CheckIn.get_random()
    last_check_in = hospody.CheckIn.get_random()

    check_ins = [last_check_in, first_check_in, middle_check_in]
    hospody.sort_check_ins(check_ins)

    assert first_check_in.dt < middle_check_in.dt < last_check_in.dt
    assert check_ins[0].dt > check_ins[1].dt > check_ins[2].dt
