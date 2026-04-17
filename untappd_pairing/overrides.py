import json
import logging
from pathlib import Path

from utils import common

logger = logging.getLogger(__name__)

OVERRIDES_PATH = Path("untappd_pairing/overrides.json")


def load(path: Path = OVERRIDES_PATH) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(common.ENCODING))
    except json.JSONDecodeError:
        logger.exception("Failed to parse overrides %s; ignoring", path)
        return {}
    if not isinstance(data, dict):
        logger.error("Overrides %s must be a JSON object; got %s", path, type(data).__name__)
        return {}
    return {str(k): str(v) for k, v in data.items()}
