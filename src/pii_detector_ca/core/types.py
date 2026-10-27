"""Framework-neutral types for identifier detection."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class PatternSpec:
    name: str
    regex: str
    score: float


@dataclass(frozen=True)
class EntitySpec:
    """Single identifier definition: patterns, context policy, and validator."""

    entity: str
    patterns: tuple[PatternSpec, ...]
    context: tuple[str, ...] = ()
    validator: Callable[[str], bool | None] | None = None
    case_sensitive: bool = False
    recognizer_name: str | None = None
    provenance_doc: str | None = None


@dataclass(frozen=True)
class Match:
    """A detected identifier span in source text."""

    entity: str
    start: int
    end: int
    score: float
    text: str
    pattern_name: str
