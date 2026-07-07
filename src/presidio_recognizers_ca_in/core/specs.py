"""Machine-readable entity definitions for Canada and India identifiers."""

from __future__ import annotations

from dataclasses import replace

from .types import EntitySpec, PatternSpec
from .validators import (
    ca_ab_uli_plausible,
    ca_bc_phn_valid,
    ca_ohip_valid,
    ca_ramq_valid,
    ca_sin_valid,
    ca_street_address_valid,
    in_aadhaar_valid,
    in_abha_plausible,
    in_mobile_valid,
    in_pan_valid,
)

_HEALTH_CONTEXT_EN = (
    "health card",
    "health number",
    "health card number",
    "hcn",
    "phn",
    "personal health number",
    "medical card",
)
_HEALTH_CONTEXT_FR = (
    "assurance maladie",
    "numéro d'assurance maladie",
    "carte soleil",
    "ramq",
)

_PROV = r"(?:AB|BC|MB|NB|NL|NS|NT|NU|ON|PE|QC|SK|YT)"
_POSTAL = r"[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?\d[ABCEGHJ-NPRSTV-Z]\d"
_FRENCH_TYPES = (
    r"(?:rue|avenue|boulevard|chemin|montée|côte|rang|place|allée|terrasse|"
    r"croissant|impasse|promenade)"
)
_ADDRESS_ANCHOR = rf",\s[^,\n]{{2,60}},\s{_PROV}\s+{_POSTAL}\b"

_DEFAULT_UHID_PATTERN = r"\b[A-Z]{2,6}[-/]?\d{5,10}\b"

_ENTITY_SPECS: dict[str, EntitySpec] = {
    "CA_SIN": EntitySpec(
        entity="CA_SIN",
        locale="ca",
        patterns=(
            PatternSpec("ca_sin_separated", r"\b\d{3}[- ]\d{3}[- ]\d{3}\b", 0.4),
            PatternSpec("ca_sin_compact", r"\b\d{9}\b", 0.1),
        ),
        context=(
            "sin",
            "social insurance",
            "social insurance number",
            "numéro d'assurance sociale",
            "nas",
        ),
        validator=ca_sin_valid,
        provenance_doc="docs/identifiers/ca_sin.md",
    ),
    "CA_OHIP": EntitySpec(
        entity="CA_OHIP",
        locale="ca",
        patterns=(
            PatternSpec(
                "ohip_separated",
                r"\b\d{4}[- ]\d{3}[- ]\d{3}(?:[- ]?[A-Z]{1,2})?\b",
                0.4,
            ),
            PatternSpec("ohip_compact", r"\b\d{10}[A-Z]{0,2}\b", 0.15),
        ),
        context=_HEALTH_CONTEXT_EN + ("ohip", "ontario health"),
        validator=ca_ohip_valid,
        provenance_doc="docs/identifiers/ca_ohip.md",
    ),
    "CA_RAMQ": EntitySpec(
        entity="CA_RAMQ",
        locale="ca",
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
        locale="ca",
        patterns=(
            PatternSpec("bc_phn_separated", r"\b9\d{3}[- ]\d{3}[- ]\d{3}\b", 0.4),
            PatternSpec("bc_phn_compact", r"\b9\d{9}\b", 0.15),
        ),
        context=_HEALTH_CONTEXT_EN + ("bc services card", "care card"),
        validator=ca_bc_phn_valid,
        provenance_doc="docs/identifiers/ca_bc_phn.md",
    ),
    "CA_AB_ULI": EntitySpec(
        entity="CA_AB_ULI",
        locale="ca",
        patterns=(
            PatternSpec("ab_uli_separated", r"\b\d{5}[- ]\d{4}\b", 0.2),
            PatternSpec("ab_uli_compact", r"\b\d{9}\b", 0.05),
        ),
        context=_HEALTH_CONTEXT_EN
        + ("health", "card", "uli", "alberta health", "ahcip"),
        validator=ca_ab_uli_plausible,
        provenance_doc="docs/identifiers/ca_ab_uli.md",
    ),
    "CA_HEALTH_CARD": EntitySpec(
        entity="CA_HEALTH_CARD",
        locale="ca",
        patterns=(PatternSpec("ca_health_generic", r"\b[A-Z]{0,2}\d{6,12}\b", 0.01),),
        context=_HEALTH_CONTEXT_EN + _HEALTH_CONTEXT_FR + ("msp", "medicare number"),
        provenance_doc="docs/identifiers/ca_health_card_generic.md",
    ),
    "CA_POSTAL_CODE": EntitySpec(
        entity="CA_POSTAL_CODE",
        locale="ca",
        patterns=(
            PatternSpec(
                "ca_postal",
                r"\b[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?\d[ABCEGHJ-NPRSTV-Z]\d\b",
                0.5,
            ),
        ),
        context=("address", "postal code", "residence", "street", "ave", "unit"),
        provenance_doc="docs/identifiers/ca_postal_code.md",
    ),
    "CA_STREET_ADDRESS": EntitySpec(
        entity="CA_STREET_ADDRESS",
        locale="ca",
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
    "IN_AADHAAR": EntitySpec(
        entity="IN_AADHAAR",
        locale="in",
        patterns=(
            PatternSpec("aadhaar_separated", r"\b[2-9]\d{3}[- ]\d{4}[- ]\d{4}\b", 0.4),
            PatternSpec("aadhaar_compact", r"\b[2-9]\d{11}\b", 0.15),
        ),
        context=(
            "aadhaar",
            "aadhar",
            "uid",
            "uidai",
            "आधार",
            "unique identification",
        ),
        validator=in_aadhaar_valid,
    ),
    "IN_ABHA": EntitySpec(
        entity="IN_ABHA",
        locale="in",
        patterns=(
            PatternSpec("abha_separated", r"\b\d{2}[- ]\d{4}[- ]\d{4}[- ]\d{4}\b", 0.4),
            PatternSpec("abha_compact", r"\b\d{14}\b", 0.1),
        ),
        context=(
            "abha",
            "health account",
            "ayushman bharat",
            "health id",
            "ndhm",
            "abdm",
            "स्वास्थ्य",
        ),
        validator=in_abha_plausible,
    ),
    "IN_PAN": EntitySpec(
        entity="IN_PAN",
        locale="in",
        patterns=(PatternSpec("pan", r"\b[A-Z]{5}\d{4}[A-Z]\b", 0.4),),
        context=("pan", "permanent account number", "income tax", "पैन"),
        validator=in_pan_valid,
        case_sensitive=True,
    ),
    "IN_UHID": EntitySpec(
        entity="IN_UHID",
        locale="in",
        patterns=(PatternSpec("uhid", _DEFAULT_UHID_PATTERN, 0.1),),
        context=(
            "uhid",
            "uh id",
            "hospital id",
            "patient id",
            "registration no",
            "mrn",
            "ipd no",
            "opd no",
        ),
    ),
    "IN_MOBILE": EntitySpec(
        entity="IN_MOBILE",
        locale="in",
        patterns=(
            PatternSpec(
                "in_mobile_prefixed",
                r"(?:\+91[- ]?|\b0)?[6-9]\d{4}[- ]?\d{5}\b",
                0.4,
            ),
        ),
        context=("mobile", "phone", "contact", "whatsapp", "मोबाइल"),
        validator=in_mobile_valid,
    ),
    "IN_PIN_CODE": EntitySpec(
        entity="IN_PIN_CODE",
        locale="in",
        patterns=(PatternSpec("in_pin", r"\b[1-9]\d{5}\b", 0.05),),
        context=("pin", "pincode", "pin code", "postal", "address", "पिन"),
    ),
    "IN_VOTER_ID": EntitySpec(
        entity="IN_VOTER_ID",
        locale="in",
        patterns=(PatternSpec("in_voter_id", r"\b[A-Z]{3}\d{7}\b", 0.4),),
        context=("voter", "epic", "election", "proof", "id proof", "मतदाता"),
        case_sensitive=True,
    ),
    "IN_PASSPORT": EntitySpec(
        entity="IN_PASSPORT",
        locale="in",
        patterns=(PatternSpec("in_passport", r"\b[A-PR-WY][1-9]\d{6}\b", 0.4),),
        context=("passport", "proof", "id proof", "पासपोर्ट"),
        case_sensitive=True,
    ),
}

ENTITY_IDS: tuple[str, ...] = tuple(_ENTITY_SPECS)


def get_entity_spec(
    entity: str,
    *,
    pattern: str | None = None,
    score: float | None = None,
) -> EntitySpec:
    """Return an entity spec, optionally overriding UHID pattern/score."""
    spec = _ENTITY_SPECS[entity]
    if entity == "IN_UHID" and (pattern is not None or score is not None):
        base = spec.patterns[0]
        return replace(
            spec,
            patterns=(
                PatternSpec(
                    base.name,
                    pattern if pattern is not None else base.regex,
                    score if score is not None else base.score,
                ),
            ),
        )
    return spec


def get_entity_specs(locales: list[str] | None = None) -> list[EntitySpec]:
    """Return entity specs for the requested locales (``ca``, ``in``)."""
    locales = [loc.lower() for loc in (locales or ["ca", "in"])]
    specs: list[EntitySpec] = []
    if "ca" in locales:
        specs.extend(s for s in _ENTITY_SPECS.values() if s.locale == "ca")
    if "in" in locales:
        specs.extend(s for s in _ENTITY_SPECS.values() if s.locale == "in")
    return specs
