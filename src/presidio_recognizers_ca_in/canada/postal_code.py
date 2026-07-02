"""Canadian postal code recognizer (address context)."""

from presidio_analyzer import Pattern

from ..base import ValidatedPatternRecognizer

# Letters D, F, I, O, Q, U never appear; first letter also excludes W and Z.
_POSTAL_REGEX = (
    r"\b[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?\d[ABCEGHJ-NPRSTV-Z]\d\b"
)


class CaPostalCodeRecognizer(ValidatedPatternRecognizer):
    def __init__(self):
        super().__init__(
            supported_entity="CA_POSTAL_CODE",
            patterns=[
                Pattern(name="ca_postal", regex=_POSTAL_REGEX, score=0.5),
            ],
            context=["address", "postal code", "residence", "street", "ave", "unit"],
            validator=None,
        )
