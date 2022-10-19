class BaseRobot:
    def run(self) -> None:
        self._main()

    def _main(self) -> None:
        raise NotImplementedError
