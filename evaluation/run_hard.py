"""Evaluate the Canadian adversarial / hard split (plan item 3.2).

Reports, per (entity, variant) cell and for stock Presidio and Presidio +
pack:

- leak recall      gold overlapped by ANY prediction (incidental DATE_TIME /
                   PHONE_NUMBER overlap counts);
- strict recall    gold fully covered by the union of predictions;
- pack recall      gold overlapped by a prediction of the gold's own type —
                   the only number that measures the pack's recognizers.

The `control` variant is the in-distribution baseline; the other variants
isolate one out-of-distribution perturbation each. Low numbers are findings,
not failures. CI gates PACK recall per variant (thresholds.json,
"hard_min_pack_recall"); leak recall is reported but not gated because it
passes even when the pack contributes nothing.

Usage:
    python benchmark/generate_hard.py --per-cell 50
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

from metrics import Span, attributed_types, fully_covered  # noqa: E402
from run_eval import build_analyzer, collect_metadata, predict_presidio  # noqa: E402

VARIANTS = [
    "control",
    "no_context",
    "unusual_separator",
    "line_wrap",
    "ocr_confusable",
    "dictation",
]
_KEYS = ("detected", "covered", "attributed")


def evaluate(notes: list[dict], predictions: list[list[Span]]) -> dict:
    """Per (entity, variant) counts. One gold entity per note."""
    cells: dict[tuple[str, str], dict] = defaultdict(
        lambda: {"gold": 0, "detected": 0, "covered": 0, "attributed": 0, "missed": []}
    )
    for note, preds in zip(notes, predictions, strict=True):
        ent = note["entities"][0]
        gold = Span(ent["start"], ent["end"], ent["type"])
        cell = cells[(ent["type"], note["variant"])]
        cell["gold"] += 1
        overlapping = [p for p in preds if p.overlaps(gold)]
        owners = attributed_types(gold.type)
        if overlapping:
            cell["detected"] += 1
        if fully_covered(gold, overlapping):
            cell["covered"] += 1
        if any(p.type in owners for p in overlapping):
            cell["attributed"] += 1
        else:
            cell["missed"].append(ent["value"])
    return dict(cells)


def by_variant(cells: dict) -> dict:
    agg: dict[str, dict] = defaultdict(lambda: {"gold": 0, **{k: 0 for k in _KEYS}})
    for (_, variant), c in cells.items():
        agg[variant]["gold"] += c["gold"]
        for k in _KEYS:
            agg[variant][k] += c[k]
    return {
        v: {
            **a,
            "recall": a["detected"] / a["gold"],
            "strict_recall": a["covered"] / a["gold"],
            "attributed_recall": a["attributed"] / a["gold"],
        }
        for v, a in agg.items()
    }


def matrix_table(system: str, cells: dict, entities: list[str]) -> list[str]:
    lines = [
        f"### {system} — pack recall [leak recall / strict recall] per entity x variant",
        "",
        "| Entity | " + " | ".join(VARIANTS) + " |",
        "|---|" + "---|" * len(VARIANTS),
    ]

    def fmt(c: dict) -> str:
        g = c["gold"]
        return (
            f"**{c['attributed'] / g:.2f}** "
            f"[{c['detected'] / g:.2f} / {c['covered'] / g:.2f}]"
        )

    for entity in entities:
        lines.append(
            f"| {entity} | " + " | ".join(fmt(cells[(entity, v)]) for v in VARIANTS) + " |"
        )
    agg = by_variant(cells)
    lines.append(
        "| **ALL** | "
        + " | ".join(
            f"**{agg[v]['attributed_recall']:.2f}** "
            f"[{agg[v]['recall']:.2f} / {agg[v]['strict_recall']:.2f}]"
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
    per_cell = len(notes) // (len(entities) * len(VARIANTS))

    lines = [
        "# Adversarial / hard split — Canada",
        "",
        f"{len(notes)} single-identifier notes ({per_cell} per entity x variant cell); "
        "checksum-valid values rendered in out-of-distribution surface forms. "
        "`control` is the in-distribution baseline.",
        "",
        "Each cell shows **pack recall** (gold overlapped by a prediction of its "
        "own type: the recognizer actually fired) followed by [leak recall / "
        "strict recall]. Leak recall counts overlap by ANY recognizer, so on "
        "degraded variants it includes incidental masking by DATE_TIME or "
        "PHONE_NUMBER; where pack recall is 0.00 the pack's own patterns "
        "contributed nothing. CI gates pack recall only.",
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
            + "  ".join(f"{v}={agg[v]['attributed_recall']:.2f}" for v in VARIANTS)
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
