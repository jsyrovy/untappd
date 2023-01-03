from dataclasses import dataclass


@dataclass
class User:
    name: str
    user_name: str
    color: str
    hidden: bool = False


USERS = (
    User("Jirka", "sejrik", "#577590"),
    User("Dan", "mencik2", "#43aa8b"),
    User("Matěj", "Mates511", "#90be6d"),
    User("Ondra", "ominar", "#f9c74f", hidden=True),
)
USER_NAMES = tuple(user.user_name for user in USERS)

VISIBLE_USERS = tuple(user for user in USERS if not user.hidden)
VISIBLE_USER_NAMES = tuple(user.user_name for user in VISIBLE_USERS)


def get(user_name: str):
    return [user for user in USERS if user.user_name == user_name][0]
