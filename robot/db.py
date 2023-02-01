from database import db
from robot.base import BaseRobot


class DbRobot(BaseRobot):
    def run(self) -> None:
        super().run()
        db.dump()
        db.close()

    def _main(self) -> None:
        raise NotImplementedError
