"""ABHA (Ayushman Bharat Health Account) number recognizer.

The clinically most relevant Indian identifier: a 14-digit national
health ID formatted XX-XXXX-XXXX-XXXX. No public checksum, so matches
are structural and rely on context words to reach reporting threshold
in the compact form.
"""

from presidio_analyzer import Pattern

from ..base import ValidatedPatternRecognizer
from ..validators import in_abha_plausible

_ABHA_CONTEXT = [
    "abha",
    "health account",
    "ayushman bharat",
    "health id",
    "ndhm",
    "abdm",
    "स्वास्थ्य",
]


class AbhaRecognizer(ValidatedPatternRecognizer):
    def __init__(self):
        super().__init__(
            supported_entity="IN_ABHA",
            patterns=[
                Pattern(
                    name="abha_separated",
                    regex=r"\b\d{2}[- ]\d{4}[- ]\d{4}[- ]\d{4}\b",
                    score=0.4,
                ),
                Pattern(
                    name="abha_compact",
                    regex=r"\b\d{14}\b",
                    score=0.1,
                ),
            ],
            context=_ABHA_CONTEXT,
            validator=in_abha_plausible,
        )
