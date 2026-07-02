"""PAN (Permanent Account Number) recognizer."""

from presidio_analyzer import Pattern

from ..base import ValidatedPatternRecognizer
from ..validators import in_pan_valid


class PanRecognizer(ValidatedPatternRecognizer):
    def __init__(self):
        super().__init__(
            supported_entity="IN_PAN",
            patterns=[
                Pattern(
                    name="pan",
                    regex=r"\b[A-Z]{5}\d{4}[A-Z]\b",
                    score=0.4,
                ),
            ],
            context=["pan", "permanent account number", "income tax", "पैन"],
            validator=in_pan_valid,
        )
