from database.orm import engine
from database.utils import dump
from robot.base import BaseRobot


class OrmRobot(BaseRobot):
    def __init__(self) -> None:
        super().__init__()
        self._engine = engine

    def run(self) -> None:
        super().run()
        dump(engine)

    def _main(self) -> None:
        raise NotImplementedError
