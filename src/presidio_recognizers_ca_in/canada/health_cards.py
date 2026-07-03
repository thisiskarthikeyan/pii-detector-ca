"""Canadian provincial health card recognizers.

Each province issues its own format. Ontario (OHIP) and BC (PHN) have
public checksums; Quebec (RAMQ) has a rigid structure that encodes the
holder's name and date of birth; Alberta's ULI has no public checksum
and is context-gated.
"""

from presidio_analyzer import Pattern

from ..base import ValidatedPatternRecognizer
from ..validators import (
    ca_ab_uli_plausible,
    ca_bc_phn_valid,
    ca_ohip_valid,
    ca_ramq_valid,
)

_HEALTH_CONTEXT_EN = [
    "health card",
    "health number",
    "health card number",
    "hcn",
    "phn",
    "personal health number",
    "medical card",
]
_HEALTH_CONTEXT_FR = [
    "assurance maladie",
    "numéro d'assurance maladie",
    "carte soleil",
    "ramq",
]


class OhipRecognizer(ValidatedPatternRecognizer):
    """Ontario: 10 digits + optional 1-2 letter version code, e.g. 1234-567-890-AB."""

    def __init__(self):
        super().__init__(
            supported_entity="CA_OHIP",
            patterns=[
                Pattern(
                    name="ohip_separated",
                    regex=r"\b\d{4}[- ]\d{3}[- ]\d{3}(?:[- ]?[A-Z]{1,2})?\b",
                    score=0.4,
                ),
                Pattern(
                    name="ohip_compact",
                    regex=r"\b\d{10}[A-Z]{0,2}\b",
                    score=0.15,
                ),
            ],
            context=_HEALTH_CONTEXT_EN + ["ohip", "ontario health"],
            validator=ca_ohip_valid,
        )


class RamqRecognizer(ValidatedPatternRecognizer):
    """Quebec: 4 letters + 8 digits, e.g. TREM 1234 5678 (LLLL YYMM DDSS)."""

    def __init__(self):
        super().__init__(
            supported_entity="CA_RAMQ",
            patterns=[
                Pattern(
                    name="ramq_separated",
                    regex=r"\b[A-ZÀ-ÖØ-Þ]{4}[- ]?\d{4}[- ]?\d{4}\b",
                    score=0.4,
                ),
            ],
            context=_HEALTH_CONTEXT_EN + _HEALTH_CONTEXT_FR,
            validator=ca_ramq_valid,
        )


class BcPhnRecognizer(ValidatedPatternRecognizer):
    """British Columbia: 10 digits starting with 9, mod-11 checksum."""

    def __init__(self):
        super().__init__(
            supported_entity="CA_BC_PHN",
            patterns=[
                Pattern(
                    name="bc_phn_separated",
                    regex=r"\b9\d{3}[- ]\d{3}[- ]\d{3}\b",
                    score=0.4,
                ),
                Pattern(
                    name="bc_phn_compact",
                    regex=r"\b9\d{9}\b",
                    score=0.15,
                ),
            ],
            context=_HEALTH_CONTEXT_EN + ["bc services card", "care card"],
            validator=ca_bc_phn_valid,
        )


class AlbertaUliRecognizer(ValidatedPatternRecognizer):
    """Alberta: 9 digits, no public checksum — only fires near context words.

    Context entries include single tokens ("health", "card", "uli") because
    Presidio's lemma-based context enhancer matches token-by-token; multi-word
    phrases such as "health card" never match as a unit.
    """

    def __init__(self):
        super().__init__(
            supported_entity="CA_AB_ULI",
            patterns=[
                Pattern(
                    name="ab_uli_separated",
                    regex=r"\b\d{5}[- ]\d{4}\b",
                    score=0.2,
                ),
                Pattern(
                    name="ab_uli_compact",
                    regex=r"\b\d{9}\b",
                    score=0.05,  # requires context boost to surface
                ),
            ],
            context=_HEALTH_CONTEXT_EN
            + ["health", "card", "uli", "alberta health", "ahcip"],
            validator=ca_ab_uli_plausible,
        )


class GenericCaHealthCardRecognizer(ValidatedPatternRecognizer):
    """Fallback for remaining provinces (SK, MB, NS, NB, NL, PE, territories).

    Formats vary (6-12 digits, some alphanumeric); fires only with strong
    context to keep precision acceptable.
    """

    def __init__(self):
        super().__init__(
            supported_entity="CA_HEALTH_CARD",
            patterns=[
                Pattern(
                    name="ca_health_generic",
                    regex=r"\b[A-Z]{0,2}\d{6,12}\b",
                    score=0.01,  # context boost required
                ),
            ],
            context=_HEALTH_CONTEXT_EN + _HEALTH_CONTEXT_FR + ["msp", "medicare number"],
            validator=None,
        )
