from dataclasses import dataclass
from typing import Literal


@dataclass
class User:
    name: str
    user_name: str
    color: str
    sex: Literal["male", "female"]
    hidden: bool = False


USERS = (
    User("Jirka", "sejrik", "#577590", "male"),
    User("Dan", "mencik2", "#43aa8b", "male"),
    User("Matěj", "Mates511", "#90be6d", "male"),
    User("Ondra", "ominar", "#f9c74f", "male", hidden=True),
    User("Kája", "karolina_matukova_7117", "#f88379", "female"),
)
USER_NAMES = tuple(user.user_name for user in USERS)

VISIBLE_USERS = tuple(user for user in USERS if not user.hidden)
VISIBLE_USER_NAMES = tuple(user.user_name for user in VISIBLE_USERS)


class UserNotFoundError(Exception):
    def __init__(self, user_name: str) -> None:
        super().__init__(f"User '{user_name}' not found.")


def get(user_name: str) -> User:
    try:
        return [user for user in USERS if user.user_name == user_name][0]  # noqa: RUF015
    except IndexError as e:
        raise UserNotFoundError(user_name) from e
