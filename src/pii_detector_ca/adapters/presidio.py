"""Presidio adapter built from framework-neutral entity specs."""

from __future__ import annotations

from typing import ClassVar

from presidio_analyzer import Pattern

from ..base import ValidatedPatternRecognizer
from ..core.specs import EntitySpec, get_entity_spec


def _recognizer_kwargs(spec: EntitySpec) -> dict:
    """Build the ``ValidatedPatternRecognizer`` constructor kwargs for a spec.

    Single source of truth for spec -> Presidio-recognizer wiring, shared by
    ``recognizer_from_spec`` and ``SpecRecognizer`` so the two never drift.
    """
    return {
        "supported_entity": spec.entity,
        "patterns": [
            Pattern(name=pattern.name, regex=pattern.regex, score=pattern.score)
            for pattern in spec.patterns
        ],
        "context": list(spec.context),
        "validator": spec.validator,
        "case_sensitive": spec.case_sensitive,
        "name": spec.recognizer_name or f"{spec.entity}Recognizer",
    }


def recognizer_from_spec(spec: EntitySpec) -> ValidatedPatternRecognizer:
    """Build a Presidio recognizer from a core entity spec."""
    return ValidatedPatternRecognizer(**_recognizer_kwargs(spec))


class SpecRecognizer(ValidatedPatternRecognizer):
    """Presidio recognizer backed by a core entity spec."""

    entity_id: ClassVar[str]

    def __init__(self) -> None:
        super().__init__(**_recognizer_kwargs(get_entity_spec(self.entity_id)))


def recognizers_from_specs(specs: list[EntitySpec]) -> list[ValidatedPatternRecognizer]:
    return [recognizer_from_spec(spec) for spec in specs]
