import argparse
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Args:
    local: bool = False
    notificationless: bool = False
    publish: bool = False


class BaseRobot:
    def __init__(self, args: Args | None = None) -> None:
        self._args = args or self._get_args()

    def run(self) -> None:
        self._main()

    def _main(self) -> None:
        raise NotImplementedError

    @staticmethod
    def _get_args() -> Args:
        parser = argparse.ArgumentParser()
        parser.add_argument("--local", action="store_true", help="don't download data from website")
        parser.add_argument("--notificationless", action="store_true", help="don't send notifications")
        parser.add_argument("--publish", action="store_true", help="publish page only")
        args, _ = parser.parse_known_args()
        return Args(local=args.local, notificationless=args.notificationless, publish=args.publish)
