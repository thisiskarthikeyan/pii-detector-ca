"""Street-address evaluation on the ODA holdout corpus (plan item 3.9).

Reports leak and strict (fully-covered) recall for gold ADDRESS spans on
notes built from real ODA rows that the main benchmark generator never uses.
Compares stock Presidio vs Presidio + pack (including CA_STREET_ADDRESS).

Writes evaluation/results/address_ca.{md,json}. Floors are gated in CI via
the address_min_strict_recall section of thresholds.json.

Usage:
    python benchmark/generate_address_eval.py --n 300
    python evaluation/run_address_eval.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "evaluation"))

from metrics import bootstrap_ci, evaluate_notes, overall  # noqa: E402
from run_eval import build_analyzer, collect_metadata, predict_presidio  # noqa: E402


def main() -> None:
    path = REPO / "benchmark" / "data" / "addresses" / "ca_address_eval.jsonl"
    if not path.exists():
        sys.exit(f"ERROR: {path} missing — run benchmark/generate_address_eval.py first.")
    with open(path, encoding="utf-8") as f:
        notes = [json.loads(line) for line in f]

    lines = [
        "# Street-address evaluation — ODA holdout (Canada)",
        "",
        f"{len(notes)} single-address notes from the ODA eval holdout "
        "(not used by the main benchmark generator). Strict recall requires "
        "the full address span to be fully covered by predictions.",
        "",
    ]
    results: dict = {}
    for system, with_pack in [("Stock Presidio", False), ("Presidio + pack", True)]:
        preds = predict_presidio(build_analyzer(with_pack=with_pack), notes)
        stats, precision, per_note = evaluate_notes(notes, preds)
        ci = bootstrap_ci(per_note)
        o = overall(stats)
        addr = stats["ADDRESS"]
        results[system] = {
            "overall": o,
            "address": {
                "gold": addr.gold,
                "detected": addr.detected,
                "covered": addr.covered,
                "recall": addr.recall,
                "strict_recall": addr.strict_recall,
            },
            "span_precision": precision,
            "bootstrap_ci_95": ci,
        }
        lines += [
            f"### {system}",
            "",
            f"ADDRESS leak recall: **{addr.recall:.3f}** "
            f"({addr.detected}/{addr.gold})",
            f"ADDRESS strict recall: **{addr.strict_recall:.3f}** "
            f"({addr.covered}/{addr.gold})",
            f"Span precision: {precision['precision']:.3f}",
            f"Bootstrap 95% CI strict recall: {ci.get('strict_recall', [])}",
            "",
        ]
        print(
            f"{system:18s}: ADDRESS leak={addr.recall:.3f} "
            f"strict={addr.strict_recall:.3f}"
        )

    out_dir = REPO / "evaluation" / "results"
    (out_dir / "address_ca.md").write_text("\n".join(lines), encoding="utf-8")
    (out_dir / "address_ca.json").write_text(
        json.dumps(
            {"metadata": collect_metadata(), "results": results},
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"\nWrote {out_dir}/address_ca.md and address_ca.json")


if __name__ == "__main__":
    main()
