import re
import unicodedata

_DEGREE_RE = re.compile(r"\d+\s*°")
_PARENS_RE = re.compile(r"\([^)]*\)")
_BATCH_RE = re.compile(r"\b(?:batch|vol\.?|série|serie)\s*#?\s*\d+", re.IGNORECASE)
_WHITESPACE_RE = re.compile(r"\s+")


def strip_diacritics(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return decomposed.encode("ascii", "ignore").decode("ascii")


def clean_beer_name(name: str) -> str:
    cleaned = _DEGREE_RE.sub(" ", name)
    cleaned = _PARENS_RE.sub(" ", cleaned)
    cleaned = _BATCH_RE.sub(" ", cleaned)
    cleaned = _WHITESPACE_RE.sub(" ", cleaned)
    return cleaned.strip()


def clean_brewery_name(brewery: str) -> str:
    cleaned = re.sub(r"\bpivovar\b", "", brewery, flags=re.IGNORECASE)
    cleaned = _WHITESPACE_RE.sub(" ", cleaned)
    return cleaned.strip()


def normalize_for_compare(text: str) -> str:
    return _WHITESPACE_RE.sub(" ", strip_diacritics(text).lower()).strip()


def build_search_queries(name: str, brewery: str) -> list[str]:
    queries: list[str] = []
    raw_name = name.strip()
    raw_brewery = brewery.strip()
    cleaned_name = clean_beer_name(raw_name)
    cleaned_brewery = clean_brewery_name(raw_brewery)

    candidates = [
        f"{raw_name} {raw_brewery}".strip() if raw_brewery else raw_name,
        f"{cleaned_name} {cleaned_brewery}".strip() if cleaned_brewery else cleaned_name,
        cleaned_name,
    ]

    for candidate in candidates:
        normalized = _WHITESPACE_RE.sub(" ", candidate).strip()
        if normalized and normalized not in queries:
            queries.append(normalized)

    return queries
