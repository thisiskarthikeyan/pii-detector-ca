"""Canadian Social Insurance Number (SIN) recognizer."""

from presidio_analyzer import Pattern

from ..base import ValidatedPatternRecognizer
from ..validators import ca_sin_valid

_SIN_PATTERNS = [
    Pattern(
        name="ca_sin_separated",
        regex=r"\b\d{3}[- ]\d{3}[- ]\d{3}\b",
        score=0.4,
    ),
    Pattern(
        name="ca_sin_compact",
        regex=r"\b\d{9}\b",
        score=0.1,  # bare 9 digits is weak evidence; checksum + context do the work
    ),
]

_SIN_CONTEXT = [
    "sin",
    "social insurance",
    "social insurance number",
    "numéro d'assurance sociale",
    "nas",
]


class CaSinRecognizer(ValidatedPatternRecognizer):
    def __init__(self):
        super().__init__(
            supported_entity="CA_SIN",
            patterns=_SIN_PATTERNS,
            context=_SIN_CONTEXT,
            validator=ca_sin_valid,
        )
