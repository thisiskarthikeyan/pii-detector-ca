"""Tests for the framework-neutral core scanner."""

from __future__ import annotations

import pytest

from pii_detector_ca import get_recognizers, scan
from pii_detector_ca.canada import (
    CaSinRecognizer,
    CaStreetAddressRecognizer,
    OhipRecognizer,
    RamqRecognizer,
)
from pii_detector_ca.core import ENTITY_IDS, get_entity_specs
from pii_detector_ca.validators import luhn_check_digit

THRESHOLD = 0.35


def presidio_hits(recognizer, text: str, entity: str):
    return recognizer.analyze(text, [entity], nlp_artifacts=None)


def core_hits(text: str, entity: str):
    return scan(text, entities=[entity], threshold=THRESHOLD)


class TestCoreScannerBasics:
    def test_entity_catalog_complete(self):
        assert len(get_entity_specs()) == 8
        assert len(ENTITY_IDS) == 8

    def test_sin_detected(self):
        base = "12345678"
        sin = base + luhn_check_digit(base)
        text = f"SIN: {sin[:3]}-{sin[3:6]}-{sin[6:]}"
        hits = core_hits(text, "CA_SIN")
        assert hits and hits[0].score >= 0.9

    def test_sin_invalid_checksum_rejected(self):
        assert not core_hits("SIN: 123-456-789", "CA_SIN")

    def test_ohip_span_excludes_trailing_word(self):
        base = "123456789"
        num = base + luhn_check_digit(base)
        value = f"{num[:4]} {num[4:7]} {num[7:]}"
        hits = core_hits(f"Health card {value} on file.", "CA_OHIP")
        assert hits and hits[0].text == value


class TestCorePresidioParity:
    """Core scanner should match Presidio pattern-level analyze().

    NOTE: ``presidio_hits`` below calls ``recognizer.analyze()`` directly, which
    only exercises pattern + ``validate_result`` — the same scope as
    ``core.scan()``. It does NOT go through ``AnalyzerEngine``, so Presidio's
    engine-level context-word score boosting never runs on either side here.
    These tests therefore only prove pattern/validator parity, not full
    end-to-end parity.
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

    def test_checksum_validators_boost_in_core(self):
        base = "12345678"
        sin = base + luhn_check_digit(base)
        hits = core_hits(f"value {sin} noted", "CA_SIN")
        assert hits and hits[0].score >= 0.9


class TestCorePackageIntegration:
    def test_scan_respects_entity_filter(self):
        base = "12345678"
        sin = base + luhn_check_digit(base)
        text = f"SIN {sin} postal M5G 2C4"
        only_postal = scan(text, entities=["CA_POSTAL_CODE"], threshold=0.0)
        assert {hit.entity for hit in only_postal} == {"CA_POSTAL_CODE"}

    def test_get_recognizers_returns_eight(self):
        assert len(get_recognizers()) == 8
