"""Canadian civic street address recognizer (plan item 3.9).

Matches full mailing/residence lines anchored by a Canadian postal code:
civic number + street name (+ type/direction), French orderings
("88, rue Lacaune"), unit prefixes, and PO boxes. Validated structurally
(postal-code letter classes + province code); no external lookup.

Entity type CA_STREET_ADDRESS maps to gold ADDRESS in the evaluation harness.
"""

from presidio_analyzer import Pattern

from ..base import ValidatedPatternRecognizer
from ..validators import ca_street_address_valid

# Canadian province / territory codes.
_PROV = r"(?:AB|BC|MB|NB|NL|NS|NT|NU|ON|PE|QC|SK|YT)"
# Canadian postal code (same letter-class rules as CaPostalCodeRecognizer).
_POSTAL = r"[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?\d[ABCEGHJ-NPRSTV-Z]\d"
# French street types that precede the street name.
_FRENCH_TYPES = (
    r"(?:rue|avenue|boulevard|chemin|montée|côte|rang|place|allée|terrasse|"
    r"croissant|impasse|promenade)"
)

_ADDRESS_CONTEXT = [
    "address",
    "residence",
    "residing",
    "home address",
    "mailing address",
    "street",
    "domicile",
    "adresse",
    "résidence",
]


class CaStreetAddressRecognizer(ValidatedPatternRecognizer):
    """Full Canadian civic address ending in province + postal code."""

    def __init__(self):
        anchor = rf",\s[^,\n]{{2,60}},\s{_PROV}\s+{_POSTAL}\b"
        super().__init__(
            supported_entity="CA_STREET_ADDRESS",
            patterns=[
                Pattern(
                    name="ca_address_english",
                    regex=(
                        rf"\b(?:PO Box \d{{1,5}}|(?:Unit \d+, )?"
                        rf"(?:\d{{1,6}}-\d{{1,6}}|\d{{1,6}})[^,\n]{{3,90}}){anchor}"
                    ),
                    score=0.55,
                ),
                Pattern(
                    name="ca_address_french",
                    regex=rf"\b\d{{1,6}},\s{_FRENCH_TYPES}\s[^,\n]{{2,60}}{anchor}",
                    score=0.55,
                ),
            ],
            context=_ADDRESS_CONTEXT,
            validator=ca_street_address_valid,
        )
