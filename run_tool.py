from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from sqlalchemy import create_engine

from database.utils import load_dump
from utils.logging import configure_logging

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)


def main() -> None:
    configure_logging()

    parser = argparse.ArgumentParser(description="Command")
    parser.add_argument("command", type=str)
    args = parser.parse_args()

    if args.command not in COMMANDS:
        logger.error("Command not found.")
        return

    COMMANDS[args.command]()


def save_db_to_file() -> None:
    db_path = Path("data/data.sqlite")
    db_path.unlink(missing_ok=True)

    engine = create_engine(f"sqlite+pysqlite:///{db_path}")
    load_dump(engine)
    logger.info("Database saved to '%s'.", db_path)


COMMANDS: dict[str, Callable[[], None]] = {
    "save-db-to-file": save_db_to_file,
}

if __name__ == "__main__":
    main()
