"""Presidio recognizers and a standalone scanner for Canadian identifiers."""

from __future__ import annotations

from collections.abc import Iterable

from .canada import get_canada_recognizers
from .core import scan
from .core.specs import ENTITY_IDS, get_entity_spec, get_entity_specs
from .core.types import EntitySpec, Match

__version__ = "0.1.0"

__all__ = [
    "add_recognizers",
    "get_recognizers",
    "scan",
    "get_entity_spec",
    "get_entity_specs",
    "ENTITY_IDS",
    "EntitySpec",
    "Match",
    "__version__",
]


def get_recognizers(exclude: Iterable[str] = ()) -> list:
    """Return Presidio recognizer instances for every Canadian entity.

    ``exclude`` drops recognizers by entity id. Presidio >= 2.2.363 ships its
    own ``CA_SIN`` recognizer and >= 2.2.365 a ``CA_POSTAL_CODE`` one (both
    disabled by default); if you enable those, exclude ours to avoid
    duplicate detections: ``get_recognizers(exclude=["CA_SIN", "CA_POSTAL_CODE"])``.
    """
    excluded = set(exclude)
    return [
        r for r in get_canada_recognizers()
        if not excluded.intersection(r.supported_entities)
    ]


def add_recognizers(registry, exclude: Iterable[str] = ()) -> None:
    """Register the Canadian recognizers on a Presidio RecognizerRegistry."""
    for recognizer in get_recognizers(exclude):
        registry.add_recognizer(recognizer)
