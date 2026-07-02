"""Shared base class: a PatternRecognizer whose matches must pass a validator."""

from __future__ import annotations

from collections.abc import Callable

from presidio_analyzer import Pattern, PatternRecognizer


class ValidatedPatternRecognizer(PatternRecognizer):
    """PatternRecognizer that runs a deterministic validator on each regex match.

    A passing validator raises the score to ``boost_score`` (near-certain);
    a failing validator invalidates the result entirely. This is what keeps
    precision high: a 12-digit number is not an Aadhaar unless its Verhoeff
    check digit is valid.
    """

    def __init__(
        self,
        *,
        supported_entity: str,
        patterns: list[Pattern],
        context: list[str] | None = None,
        validator: Callable[[str], bool] | None = None,
        boost_score: float = 0.95,
        name: str | None = None,
        supported_language: str = "en",
    ):
        self._validator = validator
        self._boost_score = boost_score
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
