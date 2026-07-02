"""Presidio recognizers for Canadian and Indian identifiers."""

from __future__ import annotations

from .canada import get_canada_recognizers
from .india import get_india_recognizers

__version__ = "0.1.0"

__all__ = ["get_recognizers", "add_recognizers", "__version__"]


def get_recognizers(locales: list[str] | None = None) -> list:
    """Return recognizer instances for the requested locales ("ca", "in")."""
    locales = [loc.lower() for loc in (locales or ["ca", "in"])]
    recognizers: list = []
    if "ca" in locales:
        recognizers.extend(get_canada_recognizers())
    if "in" in locales:
        recognizers.extend(get_india_recognizers())
    return recognizers


def add_recognizers(registry, locales: list[str] | None = None) -> None:
    """Register all recognizers on a Presidio RecognizerRegistry."""
    for recognizer in get_recognizers(locales):
        registry.add_recognizer(recognizer)
