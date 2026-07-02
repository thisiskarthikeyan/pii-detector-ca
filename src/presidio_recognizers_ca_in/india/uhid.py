"""Hospital UHID recognizer with a configurable per-facility pattern.

Indian hospitals issue their own UHID/MRN formats (e.g. ``AIIMS-12345678``,
``KH0012345``). The default pattern is a conservative heuristic that only
fires near context words; deployments should pass their facility's exact
format, mirroring per-facility MRN profiles in clinical de-id pipelines.
"""

from presidio_analyzer import Pattern

from ..base import ValidatedPatternRecognizer

_DEFAULT_UHID_PATTERN = r"\b[A-Z]{2,6}[-/]?\d{5,10}\b"

_UHID_CONTEXT = [
    "uhid",
    "uh id",
    "hospital id",
    "patient id",
    "registration no",
    "mrn",
    "ipd no",
    "opd no",
]


class UhidRecognizer(ValidatedPatternRecognizer):
    def __init__(self, pattern: str = _DEFAULT_UHID_PATTERN, score: float = 0.1):
        super().__init__(
            supported_entity="IN_UHID",
            patterns=[Pattern(name="uhid", regex=pattern, score=score)],
            context=_UHID_CONTEXT,
            validator=None,
        )
