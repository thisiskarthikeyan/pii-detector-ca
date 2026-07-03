"""Evaluate the Canadian adversarial / hard split (plan item 3.2).

Reports leak recall and strict (fully-covered) recall per (entity, variant)
cell for stock Presidio and Presidio + pack, using the same overlap/coverage
definitions as the main harness (metrics.py). The `control` variant is the
in-distribution baseline; the other variants isolate one out-of-distribution
perturbation each, so the drop from control quantifies robustness honestly —
this split exists to NOT be circular, and low numbers here are findings, not
failures.

Writes evaluation/results/hard_ca.{md,json}. Regression floors (set at the
measured values, not at 1.0) are gated in CI by check_thresholds.py using
the "hard_min_recall" section of thresholds.json.

Usage:
    python benchmark/generate_hard.py --per-cell 10
    python evaluation/run_hard.py
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "evaluation"))

from metrics import Span, fully_covered  # noqa: E402
from run_eval import build_analyzer, collect_metadata, predict_presidio  # noqa: E402

VARIANTS = [
    "control",
    "no_context",
    "unusual_separator",
    "line_wrap",
    "ocr_confusable",
    "dictation",
]


def evaluate(notes: list[dict], predictions: list[list[Span]]) -> dict:
    """Per (entity, variant) leak/strict recall. One gold entity per note."""
    cells: dict[tuple[str, str], dict] = defaultdict(
        lambda: {"gold": 0, "detected": 0, "covered": 0, "missed": []}
    )
    for note, preds in zip(notes, predictions, strict=True):
        ent = note["entities"][0]
        gold = Span(ent["start"], ent["end"], ent["type"])
        cell = cells[(ent["type"], note["variant"])]
        cell["gold"] += 1
        overlapping = [p for p in preds if p.overlaps(gold)]
        if overlapping:
            cell["detected"] += 1
        else:
            cell["missed"].append(ent["value"])
        if fully_covered(gold, overlapping):
            cell["covered"] += 1
    return dict(cells)


def by_variant(cells: dict) -> dict:
    agg: dict[str, dict] = defaultdict(lambda: {"gold": 0, "detected": 0, "covered": 0})
    for (_, variant), c in cells.items():
        agg[variant]["gold"] += c["gold"]
        agg[variant]["detected"] += c["detected"]
        agg[variant]["covered"] += c["covered"]
    return {
        v: {
            **a,
            "recall": a["detected"] / a["gold"],
            "strict_recall": a["covered"] / a["gold"],
        }
        for v, a in agg.items()
    }


def matrix_table(system: str, cells: dict, entities: list[str]) -> list[str]:
    lines = [
        f"### {system} — leak recall (strict recall) per entity x variant",
        "",
        "| Entity | " + " | ".join(VARIANTS) + " |",
        "|---|" + "---|" * len(VARIANTS),
    ]
    for entity in entities:
        row = [entity]
        for variant in VARIANTS:
            c = cells[(entity, variant)]
            row.append(f"{c['detected'] / c['gold']:.2f} ({c['covered'] / c['gold']:.2f})")
        lines.append("| " + " | ".join(row) + " |")
    agg = by_variant(cells)
    lines.append(
        "| **ALL** | "
        + " | ".join(
            f"**{agg[v]['recall']:.2f} ({agg[v]['strict_recall']:.2f})**"
            for v in VARIANTS
        )
        + " |"
    )
    lines.append("")
    return lines


def main() -> None:
    path = REPO / "benchmark" / "data" / "hard" / "ca_hard.jsonl"
    if not path.exists():
        sys.exit(f"ERROR: {path} missing — run benchmark/generate_hard.py first.")
    with open(path, encoding="utf-8") as f:
        notes = [json.loads(line) for line in f]
    entities = sorted({n["entities"][0]["type"] for n in notes})

    lines = [
        "# Adversarial / hard split — Canada",
        "",
        f"{len(notes)} single-identifier notes; checksum-valid values rendered in "
        "out-of-distribution surface forms. `control` is the in-distribution "
        "baseline; degradation from control is the honest robustness number.",
        "",
        "Interpretation caveat: leak recall counts overlap by ANY recognizer, so "
        "on degraded variants part of the remaining recall is *incidental* masking "
        "by built-in recognizers (DATE_TIME / PHONE_NUMBER happening to overlap), "
        "not identifier recognition — where the pack and stock rows are identical, "
        "the pack's own patterns contributed nothing. Strict recall (in "
        "parentheses) shows whether the value was fully covered.",
        "",
    ]
    results: dict = {}
    for system, with_pack in [("Stock Presidio", False), ("Presidio + pack", True)]:
        preds = predict_presidio(build_analyzer(with_pack=with_pack), notes)
        cells = evaluate(notes, preds)
        lines += matrix_table(system, cells, entities)
        agg = by_variant(cells)
        results[system] = {
            "by_variant": agg,
            "cells": {
                f"{entity}|{variant}": c
                for (entity, variant), c in sorted(cells.items())
            },
        }
        print(
            f"{system:18s}: "
            + "  ".join(f"{v}={agg[v]['recall']:.2f}" for v in VARIANTS)
        )

    out_dir = REPO / "evaluation" / "results"
    (out_dir / "hard_ca.md").write_text("\n".join(lines), encoding="utf-8")
    (out_dir / "hard_ca.json").write_text(
        json.dumps(
            {"metadata": collect_metadata(), "results": results},
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"\nWrote {out_dir}/hard_ca.md and hard_ca.json")


if __name__ == "__main__":
    main()
