import utils


class BaseRobot:
    def run(self) -> None:
        self._main()

    def _main(self) -> None:
        raise NotImplementedError


class DbRobot(BaseRobot):
    def __init__(self) -> None:
        self._db = utils.db.Db()

    def run(self) -> None:
        super().run()
        self._db.dump()
        self._db.close()

    def _main(self) -> None:
        raise NotImplementedError
