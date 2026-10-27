"""Machine-readable entity definitions for Canadian identifiers.

Context words: Presidio's default ``LemmaContextAwareEnhancer`` matches
context *token by token*, so a multi-word phrase such as "health card" never
fires on its own — only its individual tokens can. Every context list below
therefore carries single tokens ("health", "card", "maladie", ...) alongside
the phrases; the phrases document the intended surface form and are matched
whole by engines that support phrase context.
"""

from __future__ import annotations

from .types import EntitySpec, PatternSpec
from .validators import (
    ca_ab_uli_plausible,
    ca_bc_phn_valid,
    ca_ohip_valid,
    ca_ramq_valid,
    ca_sin_valid,
    ca_street_address_valid,
)

_HEALTH_CONTEXT_EN = (
    "health",
    "card",
    "hcn",
    "phn",
    "health card",
    "health number",
    "health card number",
    "personal health number",
    "medical card",
)
_HEALTH_CONTEXT_FR = (
    "maladie",
    "assurance",
    "soleil",
    "ramq",
    "assurance maladie",
    "numéro d'assurance maladie",
    "carte soleil",
)

_PROV = r"(?:AB|BC|MB|NB|NL|NS|NT|NU|ON|PE|QC|SK|YT)"
_POSTAL = r"[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?\d[ABCEGHJ-NPRSTV-Z]\d"
_FRENCH_TYPES = (
    r"(?:rue|avenue|boulevard|chemin|montée|côte|rang|place|allée|terrasse|"
    r"croissant|impasse|promenade)"
)
_ADDRESS_ANCHOR = rf",\s[^,\n]{{2,60}},\s{_PROV}\s+{_POSTAL}\b"

_ENTITY_SPECS: dict[str, EntitySpec] = {
    "CA_SIN": EntitySpec(
        entity="CA_SIN",
        patterns=(
            PatternSpec("ca_sin_separated", r"\b\d{3}[- ]\d{3}[- ]\d{3}\b", 0.4),
            PatternSpec("ca_sin_compact", r"\b\d{9}\b", 0.1),
        ),
        context=(
            "sin",
            "nas",
            "social insurance",
            "social insurance number",
            "numéro d'assurance sociale",
        ),
        validator=ca_sin_valid,
        provenance_doc="docs/identifiers/ca_sin.md",
    ),
    "CA_OHIP": EntitySpec(
        entity="CA_OHIP",
        patterns=(
            # Version code letters are uppercase on every Ontario card issue.
            # The pattern is compiled case-sensitively so that a lowercase
            # English word following the number ("... 897 on file") is not
            # absorbed into the span as a bogus version code.
            PatternSpec(
                "ohip_separated",
                r"\b[1-9]\d{3}[- ]\d{3}[- ]\d{3}(?:[- ]?[A-Z]{1,2})?\b",
                0.4,
            ),
            PatternSpec("ohip_compact", r"\b[1-9]\d{9}[A-Z]{0,2}\b", 0.15),
        ),
        context=_HEALTH_CONTEXT_EN + ("ohip", "ontario", "ontario health"),
        validator=ca_ohip_valid,
        case_sensitive=True,
        provenance_doc="docs/identifiers/ca_ohip.md",
    ),
    "CA_RAMQ": EntitySpec(
        entity="CA_RAMQ",
        patterns=(
            PatternSpec(
                "ramq_separated",
                r"\b[A-ZÀ-ÖØ-Þ]{4}[- ]?\d{4}[- ]?\d{4}\b",
                0.4,
            ),
        ),
        context=_HEALTH_CONTEXT_EN + _HEALTH_CONTEXT_FR,
        validator=ca_ramq_valid,
        case_sensitive=True,
        provenance_doc="docs/identifiers/ca_ramq.md",
    ),
    "CA_BC_PHN": EntitySpec(
        entity="CA_BC_PHN",
        patterns=(
            PatternSpec("bc_phn_separated", r"\b9\d{3}[- ]\d{3}[- ]\d{3}\b", 0.4),
            PatternSpec("bc_phn_compact", r"\b9\d{9}\b", 0.15),
        ),
        context=_HEALTH_CONTEXT_EN + ("bc services card", "care card", "carecard"),
        validator=ca_bc_phn_valid,
        provenance_doc="docs/identifiers/ca_bc_phn.md",
    ),
    "CA_AB_ULI": EntitySpec(
        entity="CA_AB_ULI",
        patterns=(
            PatternSpec("ab_uli_separated", r"\b\d{5}[- ]\d{4}\b", 0.2),
            PatternSpec("ab_uli_compact", r"\b\d{9}\b", 0.05),
        ),
        context=_HEALTH_CONTEXT_EN + ("uli", "alberta", "ahcip", "alberta health"),
        validator=ca_ab_uli_plausible,
        provenance_doc="docs/identifiers/ca_ab_uli.md",
    ),
    "CA_HEALTH_CARD": EntitySpec(
        entity="CA_HEALTH_CARD",
        patterns=(PatternSpec("ca_health_generic", r"\b[A-Z]{0,2}\d{6,12}\b", 0.01),),
        context=_HEALTH_CONTEXT_EN
        + _HEALTH_CONTEXT_FR
        + (
            # Provincial program names / acronyms for the nine jurisdictions
            # without a dedicated recognizer (see provenance doc).
            "msp",
            "medicare",
            "hsn",
            "phin",
            "mcp",
            "medicare number",
        ),
        provenance_doc="docs/identifiers/ca_health_card_generic.md",
    ),
    "CA_POSTAL_CODE": EntitySpec(
        entity="CA_POSTAL_CODE",
        patterns=(
            PatternSpec(
                "ca_postal",
                r"\b[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?\d[ABCEGHJ-NPRSTV-Z]\d\b",
                0.5,
            ),
        ),
        context=("address", "postal", "postal code", "residence", "street", "ave", "unit"),
        provenance_doc="docs/identifiers/ca_postal_code.md",
    ),
    "CA_STREET_ADDRESS": EntitySpec(
        entity="CA_STREET_ADDRESS",
        patterns=(
            PatternSpec(
                "ca_address_english",
                (
                    rf"\b(?:PO Box \d{{1,5}}|(?:Unit \d+, )?"
                    rf"(?:\d{{1,6}}-\d{{1,6}}|\d{{1,6}})[^,\n]{{3,90}}){_ADDRESS_ANCHOR}"
                ),
                0.55,
            ),
            PatternSpec(
                "ca_address_french",
                rf"\b\d{{1,6}},\s{_FRENCH_TYPES}\s[^,\n]{{2,60}}{_ADDRESS_ANCHOR}",
                0.55,
            ),
        ),
        context=(
            "address",
            "residence",
            "residing",
            "home address",
            "mailing address",
            "street",
            "domicile",
            "adresse",
            "résidence",
        ),
        validator=ca_street_address_valid,
        provenance_doc="docs/identifiers/ca_street_address.md",
    ),
}

ENTITY_IDS: tuple[str, ...] = tuple(_ENTITY_SPECS)


def get_entity_spec(entity: str) -> EntitySpec:
    """Return the spec for one entity id (e.g. ``"CA_SIN"``)."""
    return _ENTITY_SPECS[entity]


def get_entity_specs(entities: list[str] | None = None) -> list[EntitySpec]:
    """Return entity specs, optionally restricted to the given entity ids."""
    if entities is None:
        return list(_ENTITY_SPECS.values())
    return [_ENTITY_SPECS[e] for e in entities]
