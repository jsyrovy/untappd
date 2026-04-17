import logging

from utils.logging import configure_logging

configure_logging()

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    from untappd_pairing import UntappdPairing

    UntappdPairing().run()
