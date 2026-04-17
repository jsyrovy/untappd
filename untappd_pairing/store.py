from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any

from utils import common

if TYPE_CHECKING:
    from untappd_pairing.matcher import MatchResult
    from untappd_pairing.tap_api import TapBeer

logger = logging.getLogger(__name__)

PAIRINGS_PATH = Path("untappd_pairing/pairings.json")
SCHEMA_VERSION = 1
RETRY_AFTER = timedelta(days=7)


def beer_key(source: str, brewery: str, name: str) -> str:
    return f"{source}::{brewery}::{name}"


def _now() -> datetime:
    return datetime.now(UTC)


def _iso(value: datetime) -> str:
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass
class PairingsStore:
    pairings: dict[str, dict[str, Any]] = field(default_factory=dict)
    unmatched: dict[str, dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> PairingsStore:
        if not path.exists():
            return cls()
        try:
            data = json.loads(path.read_text(common.ENCODING))
        except json.JSONDecodeError:
            logger.exception("Failed to parse %s; starting with an empty store", path)
            return cls()
        return cls(
            pairings=dict(data.get("pairings") or {}),
            unmatched=dict(data.get("unmatched") or {}),
        )

    def is_paired(self, key: str) -> bool:
        return key in self.pairings

    def should_retry(self, key: str, now: datetime | None = None) -> bool:
        entry = self.unmatched.get(key)
        if entry is None:
            return True
        last_tried_raw = entry.get("last_tried_at")
        if not isinstance(last_tried_raw, str):
            return True
        try:
            last_tried = datetime.fromisoformat(last_tried_raw)
        except ValueError:
            return True
        return ((now or _now()) - last_tried) >= RETRY_AFTER

    def select_pending(
        self,
        beers: list[TapBeer],
        overrides: dict[str, str] | None = None,
        now: datetime | None = None,
    ) -> list[TapBeer]:
        overrides = overrides or {}
        pending: list[TapBeer] = []
        for beer in beers:
            key = beer_key(beer.source, beer.brewery, beer.name)
            if key in overrides:
                if self.pairings.get(key, {}).get("untappd_url") != overrides[key]:
                    pending.append(beer)
                continue
            if self.is_paired(key):
                continue
            if not self.should_retry(key, now=now):
                continue
            pending.append(beer)
        return pending

    def record_match(self, beer: TapBeer, result: MatchResult, query: str, now: datetime | None = None) -> None:
        key = beer_key(beer.source, beer.brewery, beer.name)
        self.pairings[key] = {
            "untappd_url": result.candidate.url,
            "untappd_name": result.candidate.name,
            "untappd_brewery": result.candidate.brewery,
            "rating": result.candidate.rating,
            "match_score": result.score,
            "matched_at": _iso(now or _now()),
            "query_used": query,
        }
        self.unmatched.pop(key, None)

    def record_unmatched(self, beer: TapBeer, reason: str, now: datetime | None = None) -> None:
        key = beer_key(beer.source, beer.brewery, beer.name)
        previous = self.unmatched.get(key, {})
        attempts = int(previous.get("attempts") or 0) + 1
        self.unmatched[key] = {
            "attempts": attempts,
            "last_tried_at": _iso(now or _now()),
            "reason": reason,
        }

    def save(self, path: Path, now: datetime | None = None) -> None:
        payload = {
            "version": SCHEMA_VERSION,
            "generated_at": _iso(now or _now()),
            "pairings": dict(sorted(self.pairings.items())),
            "unmatched": dict(sorted(self.unmatched.items())),
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_suffix(path.suffix + ".tmp")
        tmp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding=common.ENCODING)
        tmp_path.replace(path)
