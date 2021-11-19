import json
import pathlib
import random
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Dict, Any

import jinja2
from bs4 import BeautifulSoup

import utils

CHECK_INS_PATH = 'pipa/check_ins.json'

SERVING_DRAFT = 'Čepované'
SERVING_BOTTLE = 'Lahvové'
SERVING_CAN = 'Plechovkové'
SERVING_UNKNOWN = 'Nezadáno'


@dataclass
class CheckIn:
    id: int
    dt: datetime
    beer_name: str
    brewery: str
    serving: str
    beer_link: str

    @staticmethod
    def get_random():
        return CheckIn(
            random.randrange(1000),
            datetime.now(),
            'Pivo',
            'Pivovar',
            SERVING_DRAFT,
            utils.BASE_URL,
        )

    @staticmethod
    def from_json(json_: Dict[str, Any]):
        return CheckIn(
            json_['id'],
            datetime.fromisoformat(json_['dt']),
            json_['beer_name'],
            json_['brewery'],
            json_['serving'],
            json_['beer_link'],
        )

    def to_json(self):
        return {
            'id': self.id,
            'dt': self.dt.isoformat(),
            'beer_name': self.beer_name,
            'brewery': self.brewery,
            'serving': self.serving,
            'beer_link': self.beer_link,
        }


def run() -> None:
    new_check_ins = get_new_check_ins(utils.is_run_locally())
    check_ins = load_check_ins()

    for new_check_in in new_check_ins:
        if new_check_in in check_ins:
            print(f'Check in {new_check_in.id} jiz existuje.')
            continue

        check_ins.append(new_check_in)
        print(f'Novy check in {new_check_in.id} - {new_check_in.beer_name}.')

    check_ins.sort(key=lambda check_in: check_in.id, reverse=True)

    save_check_ins(check_ins)

    unique_beers_checkins: List[CheckIn] = []

    for check_in in [check_in for check_in in check_ins if check_in.serving == SERVING_DRAFT]:
        if check_in.beer_name not in [unique_beers_checkin.beer_name for unique_beers_checkin in unique_beers_checkins]:
            unique_beers_checkins.append(check_in)

    publish_page(utils.get_template('pipa.html'), 'pipa/index.html', unique_beers_checkins)


def get_new_check_ins(local: bool) -> List[CheckIn]:
    if local:
        return [CheckIn.get_random(), CheckIn.get_random(), CheckIn.get_random()]

    page = utils.download_page(f'{utils.BASE_URL}/v/u-toulave-pipy/3663231')
    return parse_check_ins(page)


def parse_check_ins(page: str) -> List[CheckIn]:
    def parse_dt(s: str) -> datetime:
        utc_dt = datetime.strptime(s, '%a, %d %b %Y %H:%M:%S %z')
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

    def get_czech_serving(en_serving: str) -> str:
        return {
            'Draft': SERVING_DRAFT,
            'Bottle': SERVING_BOTTLE,
            'Can': SERVING_CAN,
            None: SERVING_UNKNOWN,
        }.get(en_serving, en_serving)

    soup = BeautifulSoup(page, 'html.parser')

    main_stream = soup.find('div', id='main-stream')
    items = main_stream.find_all('div', class_='item')

    beers = []

    for item in items:
        check_in = item.find('div', class_='checkin')
        text = check_in.find('p', class_='text')
        links = text.find_all('a')
        checkin_comment = check_in.find('div', class_='checkin-comment')
        feedback = check_in.find('div', class_='feedback')

        id_ = int(item['data-checkin-id'])
        dt = parse_dt(feedback.find('a', class_='time').text)
        beer_name = links[1].text
        brewery = links[2].text
        serving_section = checkin_comment.find('p', class_='serving')
        serving = get_czech_serving(serving_section.find('span').text if serving_section else None)
        beer_link = f'{utils.BASE_URL}{links[1]["href"]}'

        beers.append(CheckIn(id_, dt, beer_name, brewery, serving, beer_link))

    return beers


def load_check_ins() -> List[CheckIn]:
    path = pathlib.Path(CHECK_INS_PATH)

    if not path.exists():
        return []

    return [CheckIn.from_json(check_in) for check_in in json.loads(path.read_text())['check_ins']]


def save_check_ins(check_ins: List[CheckIn]) -> None:
    data = {'check_ins': [check_in.to_json() for check_in in check_ins]}

    with open(CHECK_INS_PATH, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))


def publish_page(template: jinja2.Template, path: str, check_ins: List[CheckIn]) -> None:
    page = pathlib.Path(path)
    page.write_text(template.render(check_ins=check_ins), "UTF-8")
