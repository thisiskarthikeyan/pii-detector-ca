"""Aadhaar number recognizer (Verhoeff-validated)."""

from presidio_analyzer import Pattern

from ..base import ValidatedPatternRecognizer
from ..validators import in_aadhaar_valid

_AADHAAR_CONTEXT = [
    "aadhaar",
    "aadhar",
    "uid",
    "uidai",
    "आधार",
    "unique identification",
]


class AadhaarRecognizer(ValidatedPatternRecognizer):
    def __init__(self):
        super().__init__(
            supported_entity="IN_AADHAAR",
            patterns=[
                Pattern(
                    name="aadhaar_separated",
                    regex=r"\b[2-9]\d{3}[- ]\d{4}[- ]\d{4}\b",
                    score=0.4,
                ),
                Pattern(
                    name="aadhaar_compact",
                    regex=r"\b[2-9]\d{11}\b",
                    score=0.15,
                ),
            ],
            context=_AADHAAR_CONTEXT,
            validator=in_aadhaar_valid,
        )
