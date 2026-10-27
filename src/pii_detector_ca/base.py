"""Shared base class: a PatternRecognizer whose matches must pass a validator."""

from __future__ import annotations

import re
from collections.abc import Callable

from presidio_analyzer import Pattern, PatternRecognizer

DEFAULT_REGEX_FLAGS = re.DOTALL | re.MULTILINE | re.IGNORECASE
CASE_SENSITIVE_FLAGS = re.DOTALL | re.MULTILINE


class ValidatedPatternRecognizer(PatternRecognizer):
    """PatternRecognizer that runs a deterministic validator on each regex match.

    ``validate_result`` implements Presidio's three-state validator contract
    (``True``/``False``/``None``) over the same validators used by
    ``core.scan()``. See "Validator semantics" in
    ``docs/architecture/core_contract.md`` for the canonical description of
    what each return value means and which validators are allowed to return
    ``True`` — that doc is the source of truth; keep this docstring in sync
    with it (or delete this summary) rather than letting the two diverge.

    Presidio-specific detail not covered by that doc: a ``True`` result here
    raises the match score to Presidio's own ``PatternRecognizer.MAX_SCORE``
    (1.0), since this class overrides ``validate_result`` rather than scoring
    directly.
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
        case_sensitive: bool = False,
    ):
        """``case_sensitive=True`` disables Presidio's default IGNORECASE flag.

        Needed when a letter block is only meaningful in uppercase (e.g. the
        RAMQ surname prefix): with IGNORECASE, ordinary lowercase words
        followed by digits would satisfy the pattern.
        """
        self._validator = validator
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            # Presidio types this as list[str]; [] and None behave identically
            # (the context enhancer skips falsy context).
            context=list(context) if context else [],
            name=name or f"{supported_entity}Recognizer",
            supported_language=supported_language,
            global_regex_flags=CASE_SENSITIVE_FLAGS if case_sensitive else DEFAULT_REGEX_FLAGS,
        )

    def validate_result(self, pattern_text: str) -> bool | None:
        if self._validator is None:
            return None  # keep the pattern's own score
        return self._validator(pattern_text)
