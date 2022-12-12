import argparse
from dataclasses import dataclass


@dataclass
class Args:
    local: bool
    tweetless: bool
    publish: bool


class BaseRobot:
    def __init__(self) -> None:
        self._args = self._get_args()

    def run(self) -> None:
        self._main()

    def _main(self) -> None:
        raise NotImplementedError

    @staticmethod
    def _get_args() -> Args:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--local", action="store_true", help="don't download data from website"
        )
        parser.add_argument(
            "--tweetless", action="store_true", help="don't tweet or send message"
        )
        parser.add_argument("--publish", action="store_true", help="publish page only")
        args = parser.parse_args()
        return Args(args.local, args.tweetless, args.publish)
