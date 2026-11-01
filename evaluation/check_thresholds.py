"""Regression gate: fail CI if evaluation results drop below pinned thresholds.

Reads the results written by run_eval.py, run_hard.py, run_address_eval.py
and run_negatives.py, compares them with evaluation/thresholds.json, prints
every check with its measured value beside the floor, and writes the same
table to evaluation/results/gate_summary.md so the committed results show
what the gate actually enforced.

Checks (see thresholds.json for the rationale of each):

- pack recall per identifier entity (the owning recognizer fired), per split;
- leak recall for spaCy-dependent entities and the total;
- pack precision, pipeline precision, over-redaction;
- recognizer presence: minimum prediction count per pack type;
- hard split: pack recall per variant;
- address holdout: strict recall for the in-distribution form;
- negatives: FP rate per confusable source, and zero unplanted FPs.

The gate logic lives in ``run_checks`` so tests can exercise it on crafted
inputs (tests/test_gate.py) without Presidio installed.

Usage:
    python evaluation/run_eval.py --all
    python evaluation/run_negatives.py
    python evaluation/run_hard.py
    python evaluation/run_address_eval.py
    python evaluation/check_thresholds.py
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).parent
RESULTS = HERE / "results" / "results.json"
NEGATIVES = HERE / "results" / "negatives_ca.json"
HARD = HERE / "results" / "hard_ca.json"
ADDRESS_EVAL = HERE / "results" / "address_ca.json"
THRESHOLDS = HERE / "thresholds.json"
SUMMARY = HERE / "results" / "gate_summary.md"


@dataclass
class Check:
    group: str
    name: str
    measured: float | None
    bound: float
    op: str  # ">=" or "<="

    @property
    def ok(self) -> bool:
        if self.measured is None:
            return False
        return self.measured >= self.bound if self.op == ">=" else self.measured <= self.bound

    def line(self) -> str:
        m = "missing" if self.measured is None else f"{self.measured:.3f}"
        return f"| {self.group} | {self.name} | {m} | {self.op} {self.bound:.3f} | " + (
            "OK" if self.ok else "FAIL"
        ) + " |"


def _floors(section: dict | None) -> dict:
    return {k: v for k, v in (section or {}).items() if not k.startswith("_")}


def run_checks(
    results: dict,
    config: dict,
    hard: dict | None,
    address: dict | None,
    negatives: dict | None,
) -> list[Check]:
    system = config["system"]
    checks: list[Check] = []
    gated_runs = [r for r in results["runs"] if r["system"] == system]
    if not gated_runs:
        checks.append(Check("results", f"system {system!r} present", None, 1, ">="))
        return checks

    for run in gated_runs:
        split = run["split"]
        ents = run["entities"]
        for entity, floor in _floors(config.get("min_pack_recall")).items():
            measured = ents[entity]["attributed_recall"] if entity in ents else None
            checks.append(Check(f"pack recall {split}", entity, measured, floor, ">="))
        for entity, floor in _floors(config.get("min_leak_recall")).items():
            if entity == "TOTAL":
                measured = run["overall"]["recall"]
            else:
                measured = ents[entity]["recall"] if entity in ents else None
            checks.append(Check(f"leak recall {split}", entity, measured, floor, ">="))
        sp = run["span_precision"]
        if "min_pack_precision" in config:
            checks.append(
                Check(f"precision {split}", "pack", sp["pack"]["precision"],
                      config["min_pack_precision"], ">=")
            )
        if "min_pipeline_precision" in config:
            checks.append(
                Check(f"precision {split}", "pipeline", sp["pipeline"]["precision"],
                      config["min_pipeline_precision"], ">=")
            )
        if "max_overredaction_chars_per_note" in config:
            checks.append(
                Check(f"over-redaction {split}", "chars/note",
                      sp["overredaction"]["chars_per_note"],
                      config["max_overredaction_chars_per_note"], "<=")
            )
        if split == "generated":
            counts = sp.get("pred_counts", {})
            for ptype, floor in _floors(config.get("min_pred_counts")).items():
                c = counts.get(ptype)
                measured = float(c["tp"] + c["fp"]) if c else 0.0
                checks.append(Check("recognizer presence", ptype, measured, floor, ">="))

    hard_floors = _floors(config.get("hard_min_pack_recall"))
    if hard_floors:
        variants = (hard or {}).get("results", {}).get(system, {}).get("by_variant", {})
        for variant, floor in hard_floors.items():
            v = variants.get(variant)
            measured = v["attributed_recall"] if v else None
            checks.append(Check("hard split pack recall", variant, measured, floor, ">="))

    addr_floors = _floors(config.get("address_min_strict_recall"))
    if addr_floors:
        by_form = (address or {}).get("results", {}).get(system, {}).get("by_form", {})
        for form, floor in addr_floors.items():
            f = by_form.get(form)
            measured = f["strict_recall"] if f else None
            checks.append(Check("address strict recall", form, measured, floor, ">="))

    neg_ceilings = _floors(config.get("negatives_max_fp_rate"))
    if neg_ceilings or "negatives_max_unplanted_fp" in config:
        pack = (negatives or {}).get("results", {}).get("pack", {})
        by_source = pack.get("by_source", {})
        for source, ceiling in neg_ceilings.items():
            s = by_source.get(source)
            measured = s["fp_rate"] if s and s["fp_rate"] is not None else None
            checks.append(Check("negatives FP rate", source, measured, ceiling, "<="))
        if "negatives_max_unplanted_fp" in config:
            unplanted = by_source.get("unplanted", {}).get("fp", 0) if pack else None
            checks.append(
                Check("negatives FP", "unplanted", unplanted,
                      config["negatives_max_unplanted_fp"], "<=")
            )
    return checks


def _load(path: Path) -> dict | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def main() -> None:
    if not RESULTS.exists():
        sys.exit(f"ERROR: {RESULTS} missing — run evaluation/run_eval.py --all first.")
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    config = json.loads(THRESHOLDS.read_text(encoding="utf-8"))
    checks = run_checks(
        results, config, _load(HARD), _load(ADDRESS_EVAL), _load(NEGATIVES)
    )

    header = [
        "# Threshold gate summary",
        "",
        f"System: {config['system']}. Generated: "
        f"{results.get('metadata', {}).get('generated_at', 'n/a')}. "
        "Measured values are from the committed results files; bounds from "
        "evaluation/thresholds.json.",
        "",
        "| Group | Check | Measured | Bound | Status |",
        "|---|---|---|---|---|",
    ]
    lines = header + [c.line() for c in checks]
    failures = [c for c in checks if not c.ok]
    lines += ["", f"{len(checks)} checks, {len(failures)} failure(s)."]
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")

    for c in checks:
        m = "missing" if c.measured is None else f"{c.measured:.3f}"
        status = "OK  " if c.ok else "FAIL"
        print(f"{status} {c.group:26s} {c.name:20s} {m:>8s} {c.op} {c.bound:.3f}")
    print(f"\n{len(checks)} checks, {len(failures)} failure(s). Summary: {SUMMARY}")
    if failures:
        for c in failures:
            print(f"  FAIL: {c.group} / {c.name}")
        sys.exit(1)
    print("Threshold gate passed.")


if __name__ == "__main__":
    main()
