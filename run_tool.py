import argparse
from collections.abc import Callable
from pathlib import Path

from database.orm import dump


def main() -> None:
    parser = argparse.ArgumentParser(description="Command")
    parser.add_argument("command", type=str)
    args = parser.parse_args()

    try:
        COMMANDS[args.command]()
    except KeyError:
        print("Command not found.")


def save_db_to_file() -> None:
    db_path = Path("data/data.sql")
    db_path.unlink(missing_ok=True)

    dump(str(db_path))


COMMANDS: dict[str, Callable] = {
    "save-db-to-file": save_db_to_file,
}

if __name__ == "__main__":
    main()
