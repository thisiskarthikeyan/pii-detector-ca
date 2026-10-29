"""The CI gate must fail when a recognizer is removed.

Two layers:

1. Pure logic (no Presidio): ``run_checks`` on crafted results where a gold
   entity is fully masked by another recognizer (leak recall 1.0) but its
   own recognizer never fired (pack recall 0.0) must report a failure, and
   a pack type with zero predictions must fail the presence check.
2. End to end (needs the spaCy model): building the analyzer without the BC
   PHN recognizer drives CA_BC_PHN pack recall to 0 on the held-out split
   even though leak recall stays at 1.0 via PHONE_NUMBER.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "evaluation"))

from check_thresholds import run_checks  # noqa: E402
from metrics import Span, evaluate_notes  # noqa: E402

CONFIG = json.loads((REPO / "evaluation" / "thresholds.json").read_text(encoding="utf-8"))


def _run(entities: dict, pred_counts: dict, split: str = "generated") -> dict:
    return {
        "system": CONFIG["system"],
        "split": split,
        "entities": entities,
        "overall": {"recall": 1.0},
        "span_precision": {
            "pipeline": {"precision": 1.0},
            "pack": {"precision": 1.0},
            "overredaction": {"chars_per_note": 0.0},
            "pred_counts": pred_counts,
        },
    }


def _entity(recall: float, attributed: float) -> dict:
    return {"recall": recall, "attributed_recall": attributed, "strict_recall": recall}


def _all_good_entities() -> dict:
    ents = {e: _entity(1.0, 1.0) for e in CONFIG["min_pack_recall"] if not e.startswith("_")}
    ents.update({e: _entity(1.0, 1.0) for e in ("PERSON", "DATE")})
    return ents


def _all_good_counts() -> dict:
    return {
        t: {"tp": 100, "fp": 0} for t in CONFIG["min_pred_counts"] if not t.startswith("_")
    }


class TestGateLogic:
    def test_masked_by_other_recognizer_still_fails(self):
        ents = _all_good_entities()
        ents["CA_BC_PHN"] = _entity(recall=1.0, attributed=0.0)
        checks = run_checks({"runs": [_run(ents, _all_good_counts())]}, CONFIG, None, None, None)
        failing = {(c.group, c.name) for c in checks if not c.ok}
        assert ("pack recall generated", "CA_BC_PHN") in failing

    def test_zero_predictions_fails_presence(self):
        counts = _all_good_counts()
        counts["CA_AB_ULI"] = {"tp": 0, "fp": 0}
        checks = run_checks(
            {"runs": [_run(_all_good_entities(), counts)]}, CONFIG, None, None, None
        )
        failing = {(c.group, c.name) for c in checks if not c.ok}
        assert ("recognizer presence", "CA_AB_ULI") in failing

    def test_missing_entity_is_a_failure_not_a_pass(self):
        ents = _all_good_entities()
        del ents["CA_RAMQ"]
        checks = run_checks({"runs": [_run(ents, _all_good_counts())]}, CONFIG, None, None, None)
        assert any(c.name == "CA_RAMQ" and not c.ok for c in checks)

    def test_hard_and_negatives_missing_files_fail(self):
        checks = run_checks(
            {"runs": [_run(_all_good_entities(), _all_good_counts())]},
            CONFIG, None, None, None,
        )
        groups = {c.group for c in checks if not c.ok}
        assert "hard split pack recall" in groups
        assert "negatives FP rate" in groups
        assert "address strict recall" in groups


class TestMetricsAttribution:
    def test_attributed_requires_owning_type(self):
        note = {
            "id": "n1",
            "entities": [{"start": 4, "end": 14, "type": "CA_BC_PHN", "value": "9123456784"}],
        }
        preds = [[Span(4, 14, "PHONE_NUMBER")]]
        stats, precision, _ = evaluate_notes([note], preds)
        s = stats["CA_BC_PHN"]
        assert s.recall == 1.0 and s.strict_recall == 1.0 and s.attributed_recall == 0.0
        assert precision["pack"]["total"] == 0

    def test_duplicates_do_not_inflate_precision(self):
        note = {
            "id": "n1",
            "entities": [{"start": 0, "end": 9, "type": "CA_SIN", "value": "130692544"}],
        }
        preds = [[Span(0, 9, "CA_SIN"), Span(0, 9, "CA_HEALTH_CARD"), Span(20, 25, "NRP")]]
        _, precision, _ = evaluate_notes([note], preds)
        pipe = precision["pipeline"]
        assert (pipe["tp"], pipe["dup"], pipe["fp"]) == (1, 1, 1)
        assert pipe["precision"] == 0.5
        assert precision["pack"]["precision"] == 1.0
        assert precision["overredaction"]["chars_total"] == 5


class TestGateEndToEnd:
    @pytest.fixture(scope="class")
    @staticmethod
    def heldout():
        path = REPO / "benchmark" / "data" / "gold" / "ca_gold.jsonl"
        if not path.exists():
            pytest.skip("held-out corpus not generated")
        with open(path, encoding="utf-8") as f:
            return [json.loads(line) for line in f]

    def test_removing_bc_phn_recognizer_zeroes_pack_recall(self, heldout):
        pytest.importorskip("en_core_web_sm")
        from run_eval import build_analyzer, predict_presidio

        notes = [n for n in heldout if any(e["type"] == "CA_BC_PHN" for e in n["entities"])][:8]
        assert notes
        analyzer = build_analyzer(with_pack=True, exclude=["CA_BC_PHN"])
        stats, _, _ = evaluate_notes(notes, predict_presidio(analyzer, notes))
        s = stats["CA_BC_PHN"]
        assert s.attributed_recall == 0.0
        assert s.recall > 0.0  # masked incidentally by a built-in recognizer
