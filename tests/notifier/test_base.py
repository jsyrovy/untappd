from notifier.base import Beer, get_cleaned_beer, is_in_archive


def test_is_in_archive():
    assert is_in_archive(Beer("Three Suns", "Sibeeria"))
    assert is_in_archive(Beer("Three Suns", "Pivovar Sibeeria"))
    assert is_in_archive(Beer("24° Three Suns", "Sibeeria"))
    assert is_in_archive(Beer("Three Suns 24°", "Sibeeria pivovar"))


def test_get_cleaned_beer():
    assert get_cleaned_beer(Beer("  Beer 10° ", " pivovar Brewery  ")) == Beer("beer", "brewery")


def test_beer():
    json_ = {"name": "Test Beer", "description": "Test Brewery"}
    beer = Beer.from_json(json_)

    assert beer.name == json_["name"]
    assert beer.description == json_["description"]
    assert beer.tasted is False
    assert beer.to_json() == json_
    assert str(beer) == f"{json_['name']} 🆕\n{json_['description']}"
