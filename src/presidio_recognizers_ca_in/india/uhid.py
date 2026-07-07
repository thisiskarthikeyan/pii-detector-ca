"""Hospital UHID recognizer with a configurable per-facility pattern."""

from ..adapters.presidio import SpecRecognizer


class UhidRecognizer(SpecRecognizer):
    entity_id = "IN_UHID"

    def __init__(self, pattern: str | None = None, score: float | None = None):
        super().__init__(pattern=pattern, score=score)
