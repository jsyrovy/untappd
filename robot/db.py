from db import db
from robot.base import BaseRobot


class DbRobot(BaseRobot):
    def __init__(self) -> None:
        self._db = db

    def run(self) -> None:
        super().run()
        self._db.dump()
        self._db.close()

    def _main(self) -> None:
        raise NotImplementedError
