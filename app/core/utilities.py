"""Small domain-independent helpers."""

import re
from urllib.parse import urlsplit


def normalize_text(value: str) -> str:
    """Normalize text for exact comparisons without changing displayed data."""
    return " ".join(value.strip().lower().split())


def normalize_domain(value: str) -> str:
    """Return a canonical domain representation for comparison."""
    candidate = value.strip().lower()
    if not candidate:
        return ""
    parsed = urlsplit(candidate if "://" in candidate else f"//{candidate}")
    hostname = parsed.hostname or ""
    if hostname.startswith("www."):
        hostname = hostname[4:]
    return hostname.rstrip(".")


def extract_extension(domain: str) -> str:
    """Extract the final domain extension."""
    normalized = normalize_domain(domain)
    return normalized.rsplit(".", 1)[-1] if "." in normalized else ""


def is_valid_domain(value: str) -> bool:
    """Perform a small local validation for a domain name."""
    normalized = normalize_domain(value)
    return bool(normalized and "." in normalized and re.fullmatch(r"[a-z0-9.-]+", normalized))
