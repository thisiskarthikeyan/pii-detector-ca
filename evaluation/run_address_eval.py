"""Street-address evaluation on the ODA holdout corpus (plan item 3.9).

Reports leak, strict (fully-covered) and pack-attributed recall for gold
ADDRESS spans on notes built from real ODA rows that the main benchmark
generator never uses, broken down by surface form. ``one_line`` is the form
the CA_STREET_ADDRESS regex was written against (in-distribution); every
other form is out-of-distribution and is reported, not gated.

Writes evaluation/results/address_ca.{md,json}. The in-distribution strict
floor is gated in CI via the address_min_strict_recall section of
thresholds.json.

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
    forms = sorted({n["entities"][0].get("form", "one_line") for n in notes})

    lines = [
        "# Street-address evaluation — ODA holdout (Canada)",
        "",
        f"{len(notes)} single-address notes from the ODA eval holdout (street "
        "names never used by the main benchmark generator). `one_line` is the "
        "rendering the CA_STREET_ADDRESS regex was written against; the other "
        "forms are out-of-distribution. Strict recall requires the full address "
        "span to be fully covered; pack recall requires CA_STREET_ADDRESS itself "
        "to overlap it.",
        "",
    ]
    results: dict = {}
    for system, with_pack in [("Stock Presidio", False), ("Presidio + pack", True)]:
        preds = predict_presidio(build_analyzer(with_pack=with_pack), notes)
        stats, precision, per_note = evaluate_notes(notes, preds)
        ci = bootstrap_ci(per_note)
        o = overall(stats)
        addr = stats["ADDRESS"]
        by_form = {
            k.split("|", 1)[1]: v for k, v in precision.get("by_form", {}).items()
        }
        results[system] = {
            "overall": o,
            "address": addr.as_dict(),
            "by_form": by_form,
            "span_precision": precision,
            "bootstrap_ci_95": ci,
        }
        lines += [
            f"### {system}",
            "",
            f"ADDRESS leak recall: **{addr.recall:.3f}** ({addr.detected}/{addr.gold}); "
            f"strict recall: **{addr.strict_recall:.3f}** ({addr.covered}/{addr.gold}); "
            f"pack recall: **{addr.attributed_recall:.3f}**",
            f"Pipeline precision: {precision['pipeline']['precision']:.3f}; "
            f"pack precision: {precision['pack']['precision']:.3f}; "
            f"over-redaction {precision['overredaction']['chars_per_note']:.1f} chars/note",
            f"Bootstrap 95% CI strict recall (all forms): {ci.get('strict_recall', [])}",
            "",
            "| Form | Gold | Leak recall | Strict recall | Pack recall |",
            "|---|---|---|---|---|",
        ]
        for form in forms:
            s = by_form.get(form)
            if not s:
                continue
            tag = " (in-distribution, gated)" if form == "one_line" else ""
            lines.append(
                f"| {form}{tag} | {s['gold']} | {s['recall']:.3f} | "
                f"{s['strict_recall']:.3f} | {s['attributed_recall']:.3f} |"
            )
        lines.append("")
        print(
            f"{system:18s}: ADDRESS leak={addr.recall:.3f} strict={addr.strict_recall:.3f} "
            f"pack={addr.attributed_recall:.3f}"
        )
        for form in forms:
            s = by_form.get(form)
            if s:
                print(
                    f"  {form:20s} strict={s['strict_recall']:.3f} "
                    f"pack={s['attributed_recall']:.3f}"
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
