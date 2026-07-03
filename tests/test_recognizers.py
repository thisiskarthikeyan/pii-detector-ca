"""Pattern-level recognizer tests (no AnalyzerEngine / spaCy model needed).

PatternRecognizer.analyze() runs regex + validate_result, which is the
deterministic core we own. Context-word boosting is engine-level and is
exercised in the evaluation harness instead.
"""

import pytest

from presidio_recognizers_ca_in import get_recognizers
from presidio_recognizers_ca_in.canada import (
    AlbertaUliRecognizer,
    BcPhnRecognizer,
    CaSinRecognizer,
    CaStreetAddressRecognizer,
    OhipRecognizer,
    RamqRecognizer,
)
from presidio_recognizers_ca_in.india import (
    AadhaarRecognizer,
    AbhaRecognizer,
    InMobileRecognizer,
    PanRecognizer,
    UhidRecognizer,
)
from presidio_recognizers_ca_in.validators import (
    luhn_check_digit,
    verhoeff_check_digit,
)


def entities_found(recognizer, text, entity):
    return recognizer.analyze(text, [entity], nlp_artifacts=None)


class TestCanadianRecognizers:
    def test_sin_detected_with_high_score(self):
        base = "12345678"
        sin = base + luhn_check_digit(base)
        text = f"SIN: {sin[:3]}-{sin[3:6]}-{sin[6:]}"
        results = entities_found(CaSinRecognizer(), text, "CA_SIN")
        assert results and results[0].score >= 0.9

    def test_sin_invalid_checksum_not_reported(self):
        results = entities_found(CaSinRecognizer(), "SIN: 123-456-789", "CA_SIN")
        assert not results

    def test_ohip_detected(self):
        base = "123456789"
        num = base + luhn_check_digit(base)
        text = f"Health card {num[:4]}-{num[4:7]}-{num[7:]}-KD on file"
        results = entities_found(OhipRecognizer(), text, "CA_OHIP")
        assert results and results[0].score >= 0.9

    def test_ramq_detected(self):
        results = entities_found(
            RamqRecognizer(), "RAMQ BOUC 6551 2301 presented", "CA_RAMQ"
        )
        assert results and results[0].score >= 0.9

    def test_bc_phn_detected(self):
        rec = BcPhnRecognizer()
        for mid in range(100):
            for last in "0123456789":
                candidate = f"9234567{mid:02d}{last}"
                text = f"PHN {candidate[:4]} {candidate[4:7]} {candidate[7:]}"
                results = entities_found(rec, text, "CA_BC_PHN")
                if results:
                    assert results[0].score >= 0.9
                    return
        pytest.fail("no valid BC PHN candidate detected")

    def test_street_address_english_detected(self):
        text = "Home address: 196 Everstone Dr SW, Calgary, AB T2X 0P1"
        results = entities_found(CaStreetAddressRecognizer(), text, "CA_STREET_ADDRESS")
        assert results and results[0].score >= 0.9
        assert "196 Everstone Dr SW, Calgary, AB T2X 0P1" in text[
            results[0].start : results[0].end
        ]

    def test_street_address_french_detected(self):
        text = "Adresse: 1110, avenue Pins, Montréal, QC H2B 2X1"
        results = entities_found(CaStreetAddressRecognizer(), text, "CA_STREET_ADDRESS")
        assert results and results[0].score >= 0.9

    def test_street_address_po_box_detected(self):
        text = "Mailing address: PO Box 4521, Toronto, ON M5B 2H1"
        results = entities_found(CaStreetAddressRecognizer(), text, "CA_STREET_ADDRESS")
        assert results and results[0].score >= 0.9


class TestIndianRecognizers:
    def test_aadhaar_detected(self):
        base = "23456789012"
        aadhaar = base + verhoeff_check_digit(base)
        text = f"Aadhaar {aadhaar[:4]} {aadhaar[4:8]} {aadhaar[8:]}"
        results = entities_found(AadhaarRecognizer(), text, "IN_AADHAAR")
        assert results and results[0].score >= 0.9

    def test_aadhaar_invalid_checksum_not_reported(self):
        base = "23456789012"
        good = base + verhoeff_check_digit(base)
        bad = good[:11] + str((int(good[11]) + 1) % 10)
        text = f"Aadhaar {bad[:4]} {bad[4:8]} {bad[8:]}"
        assert not entities_found(AadhaarRecognizer(), text, "IN_AADHAAR")

    def test_abha_detected(self):
        # ABHA has no checksum: the separated-format match keeps its pattern
        # score (0.4); it is never boosted to near-certainty by the validator.
        results = entities_found(
            AbhaRecognizer(), "ABHA 12-3456-7890-1234", "IN_ABHA"
        )
        assert results
        assert 0.35 <= results[0].score < 0.9

    def test_pan_detected(self):
        results = entities_found(PanRecognizer(), "PAN ABCPE1234F", "IN_PAN")
        assert results and results[0].score >= 0.9

    def test_mobile_detected(self):
        results = entities_found(
            InMobileRecognizer(), "Contact +91 98765 43210", "IN_MOBILE"
        )
        assert results and results[0].score >= 0.9

    def test_uhid_custom_pattern(self):
        rec = UhidRecognizer(pattern=r"\bAIIMS-\d{8}\b", score=0.6)
        results = entities_found(rec, "UHID AIIMS-12345678", "IN_UHID")
        assert results


class TestContextGating:
    """Checksumless (plausibility-only) recognizers must NOT be boosted to
    near-certainty by their validator; without context words their matches
    must stay below the reporting threshold (0.35 in the eval harness)."""

    THRESHOLD = 0.35

    def test_bare_uli_stays_below_threshold(self):
        results = entities_found(
            AlbertaUliRecognizer(), "The count was 574839216 units.", "CA_AB_ULI"
        )
        assert all(r.score < self.THRESHOLD for r in results)

    def test_bare_abha_stays_below_threshold(self):
        results = entities_found(
            AbhaRecognizer(), "Invoice total 12345678901234 rupees.", "IN_ABHA"
        )
        assert all(r.score < self.THRESHOLD for r in results)

    def test_uli_repeated_digit_rejected(self):
        results = entities_found(
            AlbertaUliRecognizer(), "ULI 111111111 on file", "CA_AB_ULI"
        )
        assert not [r for r in results if r.score > 0]

    def test_abha_repeated_digit_rejected(self):
        results = entities_found(
            AbhaRecognizer(), "ABHA 22222222222222 on file", "IN_ABHA"
        )
        assert not [r for r in results if r.score > 0]

    def test_checksum_validators_still_boost(self):
        # Contrast: a checksum-validated identifier IS boosted without context.
        base = "12345678"
        sin = base + luhn_check_digit(base)
        results = entities_found(CaSinRecognizer(), f"value {sin} noted", "CA_SIN")
        assert results and results[0].score >= 0.9


class TestPackageApi:
    def test_get_recognizers_all(self):
        recs = get_recognizers()
        assert len(recs) == 16

    def test_get_recognizers_by_locale(self):
        assert len(get_recognizers(["ca"])) == 8
        assert len(get_recognizers(["in"])) == 8

    def test_entities_are_unique(self):
        entities = [e for r in get_recognizers() for e in r.supported_entities]
        assert len(entities) == len(set(entities))
