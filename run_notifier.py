from utils.logging import configure_logging

configure_logging()

from notifier import Notifier  # noqa: E402

if __name__ == "__main__":
    Notifier().run()
