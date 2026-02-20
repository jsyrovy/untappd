from utils.logging import configure_logging

configure_logging()

from pivni_valka import PivniValka  # noqa: E402

if __name__ == "__main__":
    PivniValka().run()
