"""Negative tests: confusable non-PII values must not be reported.

De-identification tools are judged on both leak rate AND over-redaction.
These tests assert that common look-alikes — credit cards (which share the
Luhn checksum with SIN/OHIP), US identifier formats, clinical numerics, and
cross-locale collisions — are not reported at or above the evaluation
harness's score threshold (0.35) by any recognizer in the pack.

Context-word boosting is engine-level and cannot fire here (pattern-level
analyze), so these tests capture the recognizers' *context-free* behavior:
exactly the situation in which a confusable value appears in running text.

Scope note: the initial pass is Canada-only (see IMPLEMENTATION_PLAN.md).
India-related cases here act as a freeze gate on current behavior; the
India confusable inventory is deliberately shallow and will be expanded in
Phase 4 (items 4.0/4.1).
"""

from __future__ import annotations

from presidio_recognizers_ca_in import get_recognizers
from presidio_recognizers_ca_in.canada import BcPhnRecognizer, CaSinRecognizer, OhipRecognizer
from presidio_recognizers_ca_in.india import AadhaarRecognizer

THRESHOLD = 0.35


def reported(text: str) -> list[tuple[str, float]]:
    """(entity, score) for every pack recognizer match at/above threshold."""
    hits = []
    for rec in get_recognizers():
        for res in rec.analyze(text, rec.supported_entities, nlp_artifacts=None):
            if res.score >= THRESHOLD:
                hits.append((res.entity_type, res.score))
    return hits


class TestFinancialConfusables:
    """Credit cards are Luhn-valid like SIN/OHIP but must not be flagged."""

    CARDS = [
        "4111 1111 1111 1111",
        "4111-1111-1111-1111",
        "4111111111111111",
        "4242 4242 4242 4242",
        "5500 0055 5555 5559",
    ]

    def test_credit_cards_not_reported_by_any_recognizer(self):
        for card in self.CARDS:
            assert reported(f"Payment card {card} on file.") == [], card

    def test_invoice_number_not_reported(self):
        assert reported("Invoice INV-2026-000123 issued for services.") == []


class TestUsFormats:
    def test_us_ssn_not_reported(self):
        assert reported("US SSN 123-45-6789 provided for insurance.") == []

    def test_us_phone_not_reported(self):
        # 416-555-0192 is not Luhn-valid, so OHIP's compact 10-digit
        # pattern must reject it; the 3-3-4 grouping never matches SIN.
        for phone in ["416-555-0192", "(416) 555-0192", "4165550192"]:
            assert reported(f"Callback number {phone}.") == [], phone


class TestChecksumRejects:
    def test_luhn_invalid_sin_not_reported(self):
        results = CaSinRecognizer().analyze(
            "SIN: 123-456-789", ["CA_SIN"], nlp_artifacts=None
        )
        assert not results

    def test_luhn_invalid_ohip_not_reported(self):
        results = OhipRecognizer().analyze(
            "Health card 1234-567-890-KD", ["CA_OHIP"], nlp_artifacts=None
        )
        assert not results

    def test_verhoeff_invalid_aadhaar_not_reported(self):
        results = AadhaarRecognizer().analyze(
            "Aadhaar 4111 1111 1111", ["IN_AADHAAR"], nlp_artifacts=None
        )
        assert not results

    def test_structurally_invalid_bc_phn_not_reported(self):
        # Check digit computes to 11 (never issued) for this base.
        results = BcPhnRecognizer().analyze(
            "PHN 9123 456 789", ["CA_BC_PHN"], nlp_artifacts=None
        )
        assert not results


class TestCrossLocaleCollisions:
    def test_indian_mobile_not_reported_as_bc_phn(self):
        # Valid Indian mobile starting with 9 has BC PHN's shape; the
        # mod-11 checksum must reject it.
        results = BcPhnRecognizer().analyze(
            "Contact 9876543210", ["CA_BC_PHN"], nlp_artifacts=None
        )
        assert not results


class TestClinicalNumerics:
    """Realistic non-PII clinical content must produce no reports at all."""

    SNIPPETS = [
        "Diagnoses: E11.9, I10, J45.909 per ICD-10 coding.",
        "Labs: WBC 11.2, HbA1c 6.8%, eGFR 88 mL/min/1.73m2.",
        "BP 120/80 mmHg, HR 72 bpm, SpO2 98% on room air.",
        "Follow-up CT in 12 months; nodule measures 6 mm, previously 5 mm.",
        "Accession ACC-2026-0001 reported at 14:35 on the PACS worklist.",
    ]

    def test_clinical_snippets_produce_no_reports(self):
        for snippet in self.SNIPPETS:
            assert reported(snippet) == [], snippet
