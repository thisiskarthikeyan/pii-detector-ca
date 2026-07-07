"""Tests for the framework-neutral core scanner."""

from __future__ import annotations

import pytest

from presidio_recognizers_ca_in import get_recognizers, scan
from presidio_recognizers_ca_in.canada import (
    CaSinRecognizer,
    CaStreetAddressRecognizer,
    OhipRecognizer,
    RamqRecognizer,
)
from presidio_recognizers_ca_in.core import ENTITY_IDS, get_entity_specs
from presidio_recognizers_ca_in.india import AadhaarRecognizer, PanRecognizer
from presidio_recognizers_ca_in.validators import luhn_check_digit, verhoeff_check_digit

THRESHOLD = 0.35


def presidio_hits(recognizer, text: str, entity: str):
    return recognizer.analyze(text, [entity], nlp_artifacts=None)


def core_hits(text: str, entity: str):
    return scan(text, entities=[entity], threshold=THRESHOLD)


class TestCoreScannerBasics:
    def test_entity_catalog_complete(self):
        assert len(get_entity_specs()) == 16
        assert len(ENTITY_IDS) == 16

    def test_sin_detected(self):
        base = "12345678"
        sin = base + luhn_check_digit(base)
        text = f"SIN: {sin[:3]}-{sin[3:6]}-{sin[6:]}"
        hits = core_hits(text, "CA_SIN")
        assert hits and hits[0].score >= 0.9

    def test_sin_invalid_checksum_rejected(self):
        assert not core_hits("SIN: 123-456-789", "CA_SIN")

    def test_aadhaar_detected(self):
        base = "23456789012"
        aadhaar = base + verhoeff_check_digit(base)
        text = f"Aadhaar {aadhaar[:4]} {aadhaar[4:8]} {aadhaar[8:]}"
        hits = core_hits(text, "IN_AADHAAR")
        assert hits and hits[0].score >= 0.9


class TestCorePresidioParity:
    """Core scanner should match Presidio pattern-level analyze().

    NOTE: ``presidio_hits`` below calls ``recognizer.analyze()`` directly, which
    only exercises pattern + ``validate_result`` — the same scope as
    ``core.scan()``. It does NOT go through ``AnalyzerEngine``, so Presidio's
    engine-level context-word score boosting never runs on either side here.
    These tests therefore only prove pattern/validator parity, not full
    end-to-end parity. If/when the core scanner gains its own context-window
    scoring (see ``docs/architecture/core_contract.md``), add a companion test
    here that drives an ``AnalyzerEngine`` with context words in the text and
    compares its boosted score against ``core.scan()``'s, so a future
    Presidio-integration change can't silently drift from the core behavior.
    """

    @pytest.mark.parametrize(
        ("recognizer_cls", "entity", "text"),
        [
            (CaSinRecognizer, "CA_SIN", "SIN: 123-456-789"),
            (
                OhipRecognizer,
                "CA_OHIP",
                "Health card 1234-567-890-KD on file",
            ),
            (RamqRecognizer, "CA_RAMQ", "RAMQ BOUC 6551 2301 presented"),
            (
                CaStreetAddressRecognizer,
                "CA_STREET_ADDRESS",
                "Home address: 196 Everstone Dr SW, Calgary, AB T2X 0P1",
            ),
            (AadhaarRecognizer, "IN_AADHAAR", "Aadhaar 2345 6789 0123"),
            (PanRecognizer, "IN_PAN", "PAN ABCPE1234F"),
        ],
    )
    def test_presidio_and_core_agree_on_presence(self, recognizer_cls, entity, text):
        recognizer = recognizer_cls()
        presidio = presidio_hits(recognizer, text, entity)
        core = core_hits(text, entity)
        assert bool(presidio) == bool(core)

    def test_bare_uli_stays_below_threshold_in_core(self):
        hits = core_hits("The count was 574839216 units.", "CA_AB_ULI")
        assert all(hit.score < THRESHOLD for hit in hits)

    def test_bare_abha_stays_below_threshold_in_core(self):
        hits = core_hits("Invoice total 12345678901234 rupees.", "IN_ABHA")
        assert all(hit.score < THRESHOLD for hit in hits)

    def test_checksum_validators_boost_in_core(self):
        base = "12345678"
        sin = base + luhn_check_digit(base)
        hits = core_hits(f"value {sin} noted", "CA_SIN")
        assert hits and hits[0].score >= 0.9


class TestCorePackageIntegration:
    def test_scan_respects_locale_filter(self):
        text = "SIN 123-456-789 and Aadhaar 2345 6789 0123"
        ca_only = scan(text, locales=["ca"], threshold=0.0)
        assert all(hit.entity.startswith("CA_") for hit in ca_only)

    def test_get_recognizers_still_returns_sixteen(self):
        assert len(get_recognizers()) == 16
