"""Presidio-free regex + validator scanner."""

from __future__ import annotations

import re
from functools import lru_cache

from .specs import get_entity_specs
from .types import EntitySpec, Match

MAX_SCORE = 1.0
DEFAULT_THRESHOLD = 0.35

_DEFAULT_FLAGS = re.DOTALL | re.MULTILINE | re.IGNORECASE
_CASE_SENSITIVE_FLAGS = re.DOTALL | re.MULTILINE


@lru_cache(maxsize=64)
def _compiled_pattern(regex: str, case_sensitive: bool) -> re.Pattern[str]:
    flags = _CASE_SENSITIVE_FLAGS if case_sensitive else _DEFAULT_FLAGS
    return re.compile(regex, flags)


def _score_match(pattern_score: float, validator_result: bool | None) -> float | None:
    """Apply three-state validator semantics (matches Presidio adapter)."""
    if validator_result is False:
        return None
    if validator_result is True:
        return MAX_SCORE
    return pattern_score


def scan_entity(
    text: str,
    spec: EntitySpec,
    *,
    threshold: float = 0.0,
) -> list[Match]:
    """Scan text for one entity type using regex + validator only."""
    matches: list[Match] = []
    for pattern in spec.patterns:
        compiled = _compiled_pattern(pattern.regex, spec.case_sensitive)
        for found in compiled.finditer(text):
            value = found.group()
            score = _score_match(pattern.score, spec.validator(value) if spec.validator else None)
            if score is None or score < threshold:
                continue
            matches.append(
                Match(
                    entity=spec.entity,
                    start=found.start(),
                    end=found.end(),
                    score=score,
                    text=value,
                    pattern_name=pattern.name,
                )
            )
    return matches


def scan(
    text: str,
    *,
    locales: list[str] | None = None,
    entities: list[str] | None = None,
    threshold: float = DEFAULT_THRESHOLD,
) -> list[Match]:
    """Detect locale-specific identifiers without Presidio or spaCy."""
    specs = get_entity_specs(locales)
    if entities is not None:
        allowed = set(entities)
        specs = [spec for spec in specs if spec.entity in allowed]

    best: dict[tuple[str, int, int], Match] = {}
    for spec in specs:
        for match in scan_entity(text, spec, threshold=0.0):
            if match.score < threshold:
                continue
            key = (match.entity, match.start, match.end)
            existing = best.get(key)
            if existing is None or match.score > existing.score:
                best[key] = match

    return sorted(best.values(), key=lambda m: (m.start, m.end, m.entity))
