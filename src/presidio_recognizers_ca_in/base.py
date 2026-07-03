"""Shared base class: a PatternRecognizer whose matches must pass a validator."""

from __future__ import annotations

from collections.abc import Callable

from presidio_analyzer import Pattern, PatternRecognizer


class ValidatedPatternRecognizer(PatternRecognizer):
    """PatternRecognizer that runs a deterministic validator on each regex match.

    Validators are three-state, matching Presidio's ``validate_result`` contract:

    - ``True`` — the value passed a real integrity check (checksum / rigid
      structure). Presidio raises the match score to ``MAX_SCORE``.
    - ``False`` — the value failed the check; the match is invalidated.
    - ``None`` — no integrity check applies (plausibility-only); the pattern's
      own score is kept, so weak patterns still need context-word boosting to
      reach the reporting threshold.

    Checksum validators (SIN, OHIP, Aadhaar, ...) return True/False.
    Plausibility validators (Alberta ULI, ABHA) must return None/False — never
    True — so that a bare digit string is not boosted to near-certainty without
    supporting context.
    """

    def __init__(
        self,
        *,
        supported_entity: str,
        patterns: list[Pattern],
        context: list[str] | None = None,
        validator: Callable[[str], bool | None] | None = None,
        name: str | None = None,
        supported_language: str = "en",
    ):
        self._validator = validator
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            name=name or f"{supported_entity}Recognizer",
            supported_language=supported_language,
        )

    def validate_result(self, pattern_text: str) -> bool | None:
        if self._validator is None:
            return None  # keep the pattern's own score
        return self._validator(pattern_text)
