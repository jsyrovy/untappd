from utils.logging import configure_logging

configure_logging()

from archivist import Archivist  # noqa: E402

if __name__ == "__main__":
    Archivist().run()
