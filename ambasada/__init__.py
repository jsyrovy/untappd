import json
import pathlib
from dataclasses import dataclass
from typing import Optional

from bs4 import BeautifulSoup

import utils

BEERS_PATH = 'ambasada/beers.json'


@dataclass
class Beer:
    name: str = ''
    description: str = ''

    @staticmethod
    def from_json(json_: dict[str, str]) -> 'Beer':
        return Beer(
            json_['name'],
            json_['description'],
        )

    def to_json(self) -> dict[str, str]:
        return {
            'name': self.name,
            'description': self.description,
        }


def run() -> None:
    page = utils.download_page('https://pivniambasada.cz')

    previous_beers = load_beers()
    current_beers = get_current_beers(page)

    new_beers = [current_beer for current_beer in current_beers if current_beer not in previous_beers]
    print(new_beers)

    sort_beers(current_beers)
    save_beers(current_beers)


def get_current_beers(page: str) -> list[Beer]:
    soup = BeautifulSoup(page, 'html.parser')

    table = soup.find_all('table', class_='listek_tab')[0]
    rows = table.find_all('tr')

    beers = []
    current_beer = Beer()

    for row in rows:
        if row.find('td', class_='listek_tab_nadpis'):
            break

        if name := row.find('td', class_='listek_tab_nazev'):
            current_beer.name = name.text.strip()

        if description := row.find('td', class_='listek_tab_popis'):
            current_beer.description = description.text.strip()
            beers.append(current_beer)
            current_beer = Beer()

    return beers


def load_beers() -> list[Beer]:
    path = pathlib.Path(BEERS_PATH)

    if not path.exists():
        return []

    return [Beer.from_json(beer) for beer in json.loads(path.read_text())['beers']]


def sort_beers(beers: list[Beer]) -> None:
    beers.sort(key=lambda beer: beer.name)


def save_beers(beers: list[Beer]) -> None:
    data = {'beers': [beer.to_json() for beer in beers]}

    with open(BEERS_PATH, 'w', encoding=utils.ENCODING) as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))
