from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING

from sqlalchemy import create_engine

from database.utils import load_dump

if TYPE_CHECKING:
    from collections.abc import Callable


def main() -> None:
    parser = argparse.ArgumentParser(description="Command")
    parser.add_argument("command", type=str)
    args = parser.parse_args()

    try:
        COMMANDS[args.command]()
    except KeyError:
        print("Command not found.")


def save_db_to_file() -> None:
    db_path = Path("data/data.sqlite")
    db_path.unlink(missing_ok=True)

    engine = create_engine(f"sqlite+pysqlite:///{db_path}")
    load_dump(engine)
    print(f"Database saved to '{db_path}'.")


COMMANDS: dict[str, Callable[[], None]] = {
    "save-db-to-file": save_db_to_file,
}

if __name__ == "__main__":
    main()
