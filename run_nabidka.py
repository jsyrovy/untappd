import logging
from pathlib import Path

from utils.common import get_template
from utils.logging import configure_logging

configure_logging()

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    template = get_template("nabidka.html")
    page = template.render(active_page="nabidka")

    output = Path("nabidka.html")
    with output.open("w") as f:
        f.write(page)

    logger.info("Written: %s", output)
