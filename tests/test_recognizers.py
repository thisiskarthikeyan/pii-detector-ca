"""Pattern-level recognizer tests (no AnalyzerEngine / spaCy model needed).

PatternRecognizer.analyze() runs regex + validate_result, which is the
deterministic core we own. Context-word boosting is engine-level; a small
engine-level check lives in ``TestEngineContext`` and is skipped when the
spaCy model is not installed.
"""

import pytest

from pii_detector_ca import get_recognizers
from pii_detector_ca.canada import (
    AlbertaUliRecognizer,
    BcPhnRecognizer,
    CaSinRecognizer,
    CaStreetAddressRecognizer,
    GenericCaHealthCardRecognizer,
    OhipRecognizer,
    RamqRecognizer,
)
from pii_detector_ca.validators import luhn_check_digit


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
        assert text[results[0].start : results[0].end] == f"{num[:4]}-{num[4:7]}-{num[7:]}-KD"

    @pytest.mark.parametrize("tail", ["on file", "is valid", "at triage", "to follow", "in chart"])
    def test_ohip_span_excludes_trailing_english_words(self, tail):
        # Regression: with IGNORECASE the optional version-code group absorbed
        # any following 1-2 letter word ("... 897 on") into a 1.0-score span.
        base = "123456789"
        num = base + luhn_check_digit(base)
        value = f"{num[:4]} {num[4:7]} {num[7:]}"
        text = f"Health card {value} {tail}."
        results = entities_found(OhipRecognizer(), text, "CA_OHIP")
        assert results
        assert text[results[0].start : results[0].end] == value

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

    def test_bare_generic_health_card_stays_below_threshold(self):
        results = entities_found(
            GenericCaHealthCardRecognizer(), "Order 123456789 shipped.", "CA_HEALTH_CARD"
        )
        assert all(r.score < self.THRESHOLD for r in results)

    def test_uli_repeated_digit_rejected(self):
        results = entities_found(
            AlbertaUliRecognizer(), "ULI 111111111 on file", "CA_AB_ULI"
        )
        assert not [r for r in results if r.score > 0]

    def test_checksum_validators_still_boost(self):
        # Contrast: a checksum-validated identifier IS boosted without context.
        base = "12345678"
        sin = base + luhn_check_digit(base)
        results = entities_found(CaSinRecognizer(), f"value {sin} noted", "CA_SIN")
        assert results and results[0].score >= 0.9


class TestEngineContext:
    """Engine-level context boosting. Presidio's lemma enhancer matches single
    tokens only, so every context list must contain single tokens that
    actually fire (regression for CA_HEALTH_CARD and the French terms)."""

    THRESHOLD = 0.35

    @pytest.fixture(scope="class")
    @staticmethod
    def analyzer():
        pytest.importorskip("en_core_web_sm")
        from presidio_analyzer import AnalyzerEngine
        from presidio_analyzer.nlp_engine import NlpEngineProvider

        from pii_detector_ca import add_recognizers

        nlp = NlpEngineProvider(
            nlp_configuration={
                "nlp_engine_name": "spacy",
                "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
            }
        ).create_engine()
        engine = AnalyzerEngine(nlp_engine=nlp, supported_languages=["en"])
        add_recognizers(engine.registry)
        return engine

    def _hits(self, analyzer, text):
        res = analyzer.analyze(text=text, language="en", score_threshold=self.THRESHOLD)
        return {r.entity_type for r in res}

    def test_generic_health_card_context_is_not_attributed_to_alberta(self, analyzer):
        # "health card" alone cannot attribute a 9-digit number to a province:
        # report the generic label only, never CA_AB_ULI.
        for text in [
            "Health card 574839216 recorded at registration.",
            "Health card 57483-9216 recorded at registration.",
        ]:
            hits = self._hits(analyzer, text)
            assert "CA_HEALTH_CARD" in hits, text
            assert "CA_AB_ULI" not in hits, text

    def test_alberta_context_surfaces_uli(self, analyzer):
        for text in [
            "Alberta health card 574839216 recorded.",
            "ULI 57483-9216 on file.",
            "AHCIP number 574839216.",
        ]:
            assert "CA_AB_ULI" in self._hits(analyzer, text), text

    def test_french_context_surfaces_generic(self, analyzer):
        hits = self._hits(analyzer, "Numéro d'assurance maladie 574839216 présenté.")
        assert "CA_HEALTH_CARD" in hits

    def test_provincial_program_context(self, analyzer):
        hits = self._hits(analyzer, "MSP number 574839216 verified.")
        assert "CA_HEALTH_CARD" in hits

    def test_no_context_no_generic(self, analyzer):
        hits = self._hits(analyzer, "The count was 574839216 units.")
        assert "CA_HEALTH_CARD" not in hits
        assert "CA_AB_ULI" not in hits


class TestPackageApi:
    def test_get_recognizers_all(self):
        assert len(get_recognizers()) == 8

    def test_get_recognizers_exclude(self):
        recs = get_recognizers(exclude=["CA_SIN", "CA_POSTAL_CODE"])
        assert len(recs) == 6
        assert not any("CA_SIN" in r.supported_entities for r in recs)

    def test_entities_are_unique(self):
        entities = [e for r in get_recognizers() for e in r.supported_entities]
        assert len(entities) == len(set(entities))
