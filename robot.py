import utils


class BaseRobot:
    def run(self) -> None:
        self._main()

    def _main(self) -> None:
        raise NotImplementedError


class DbRobot(BaseRobot):
    def __init__(self) -> None:
        self.db = utils.db.Db()

    def run(self) -> None:
        super().run()
        self.db.close()

    def _main(self) -> None:
        raise NotImplementedError
