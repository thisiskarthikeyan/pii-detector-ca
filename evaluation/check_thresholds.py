"""Regression gate: fail CI if evaluation results drop below pinned thresholds.

Reads evaluation/results/results.json (written by run_eval.py) and
evaluation/thresholds.json. For every run of the gated system, each entity's
recall must meet its per-locale floor, and span precision must meet the global
floor. An entity listed in the thresholds but absent from the results is a
failure too (a silently dropped recognizer must not pass).

Usage:
    python evaluation/run_eval.py --all
    python evaluation/check_thresholds.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
RESULTS = HERE / "results" / "results.json"
NEGATIVES = HERE / "results" / "negatives_ca.json"
HARD = HERE / "results" / "hard_ca.json"
THRESHOLDS = HERE / "thresholds.json"


def main() -> None:
    if not RESULTS.exists():
        sys.exit(f"ERROR: {RESULTS} missing — run evaluation/run_eval.py --all first.")
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    config = json.loads(THRESHOLDS.read_text(encoding="utf-8"))

    system = config["system"]
    min_precision = config["min_span_precision"]
    failures: list[str] = []
    checked = 0

    gated_runs = [r for r in results["runs"] if r["system"] == system]
    if not gated_runs:
        sys.exit(f"ERROR: no runs for system {system!r} in {RESULTS}.")

    for run in gated_runs:
        locale, split = run["locale"], run["split"]
        floors = config["min_recall"].get(locale)
        if floors is None:
            continue
        tag = f"{system} {locale}/{split}"

        for entity, floor in floors.items():
            if entity == "TOTAL":
                actual = run["overall"]["recall"]
            elif entity in run["entities"]:
                actual = run["entities"][entity]["recall"]
            else:
                failures.append(f"{tag}: entity {entity} missing from results")
                continue
            checked += 1
            status = "OK  " if actual >= floor else "FAIL"
            print(f"{status} {tag:34s} {entity:12s} recall {actual:.3f} >= {floor:.2f}")
            if actual < floor:
                failures.append(
                    f"{tag}: {entity} recall {actual:.3f} below floor {floor:.2f}"
                )

        precision = run["span_precision"]["precision"]
        checked += 1
        status = "OK  " if precision >= min_precision else "FAIL"
        print(
            f"{status} {tag:34s} {'PRECISION':12s} span   {precision:.3f} >= "
            f"{min_precision:.2f}"
        )
        if precision < min_precision:
            failures.append(
                f"{tag}: span precision {precision:.3f} below floor {min_precision:.2f}"
            )

    hard_floors = {
        k: v for k, v in config.get("hard_min_recall", {}).items()
        if not k.startswith("_")
    }
    if hard_floors:
        if not HARD.exists():
            failures.append(f"hard-split results missing: {HARD}")
        else:
            hard = json.loads(HARD.read_text(encoding="utf-8"))["results"]
            if system not in hard:
                failures.append(f"hard split: system {system!r} missing from results")
            else:
                variants = hard[system]["by_variant"]
                for variant, floor in hard_floors.items():
                    if variant not in variants:
                        failures.append(f"hard split: variant {variant!r} missing")
                        continue
                    actual = variants[variant]["recall"]
                    checked += 1
                    status = "OK  " if actual >= floor else "FAIL"
                    print(
                        f"{status} hard ca {variant:26s} recall {actual:.3f} >= {floor:.2f}"
                    )
                    if actual < floor:
                        failures.append(
                            f"hard ca {variant}: recall {actual:.3f} below "
                            f"floor {floor:.2f}"
                        )

    fp_ceilings = {
        k: v
        for k, v in config.get("negatives_max_fp_per_100_notes", {}).items()
        if not k.startswith("_")
    }
    if fp_ceilings:
        if not NEGATIVES.exists():
            failures.append(f"negatives results missing: {NEGATIVES}")
        else:
            neg = json.loads(NEGATIVES.read_text(encoding="utf-8"))["results"]
            for cfg, ceiling in fp_ceilings.items():
                if cfg not in neg:
                    failures.append(f"negatives: config {cfg!r} missing from results")
                    continue
                actual = neg[cfg]["fp_per_100_notes"]
                checked += 1
                status = "OK  " if actual <= ceiling else "FAIL"
                print(f"{status} negatives {cfg:24s} FP/100 notes {actual:.2f} <= {ceiling}")
                if actual > ceiling:
                    failures.append(
                        f"negatives {cfg}: {actual:.2f} FPs/100 notes above "
                        f"ceiling {ceiling}"
                    )

    print(f"\n{checked} checks, {len(failures)} failure(s).")
    if failures:
        for f in failures:
            print(f"  FAIL: {f}")
        sys.exit(1)
    print("Threshold gate passed.")


if __name__ == "__main__":
    main()
