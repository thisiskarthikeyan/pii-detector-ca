"""Evaluate the framework-neutral core scanner (no Presidio / spaCy).

Runs the same benchmark corpora as ``run_eval.py`` but uses ``core.scan()``
for pack identifier detection only. Gold is restricted to the entities the
core can own (pack identifiers plus ADDRESS, which CA_STREET_ADDRESS maps
to); PERSON/DATE need spaCy and are excluded from both gold and precision.
Context-gated entities (CA_AB_ULI) are expected to score ~0 here because the
core applies no context boosting — that is a documented property of
``scan()``, not a regression.

Usage:
    python evaluation/run_core_eval.py --all
    python evaluation/run_core_eval.py --split gold
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "evaluation"))

from metrics import TYPE_MAP, Span, bootstrap_ci, evaluate_notes, overall  # noqa: E402

from pii_detector_ca.core import scan  # noqa: E402
from pii_detector_ca.core.specs import ENTITY_IDS  # noqa: E402

DEFAULT_THRESHOLD = 0.35
# Gold entity types the core scanner can own (pack ids, with
# CA_STREET_ADDRESS reported under the gold label ADDRESS).
CORE_GOLD_TYPES = frozenset(TYPE_MAP.get(e, e) for e in ENTITY_IDS)


def load_notes(split: str) -> list[dict]:
    if split == "gold":
        path = REPO / "benchmark" / "data" / "gold" / "ca_gold.jsonl"
    else:
        path = REPO / "benchmark" / "data" / "generated" / "ca.jsonl"
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def predict_core(notes: list[dict]) -> list[list[Span]]:
    predictions: list[list[Span]] = []
    for note in notes:
        matches = scan(note["text"], threshold=DEFAULT_THRESHOLD)
        predictions.append(
            [Span(m.start, m.end, TYPE_MAP.get(m.entity, m.entity)) for m in matches]
        )
    return predictions


def format_table(split: str, stats: dict, precision: dict, ci: dict) -> str:
    lines = [
        f"### Core scanner — split={split}",
        "",
        "Pack identifier entities + ADDRESS only (framework-neutral core; "
        "no spaCy PERSON/DATE). CA_AB_ULI is context-gated and expected ~0 here.",
        "",
        "| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate |",
        "|---|---|---|---|---|---|",
    ]
    for entity in sorted(stats):
        s = stats[entity]
        lines.append(
            f"| {entity} | {s.gold} | {s.detected} | {s.recall:.3f} | "
            f"{s.strict_recall:.3f} | {s.fn_rate:.3f} |"
        )
    o = overall(stats)
    lines.append(
        f"| **TOTAL (pack ids)** | {o['gold']} | {o['detected']} | {o['recall']:.3f} | "
        f"{o['strict_recall']:.3f} | {o['fn_rate']:.3f} |"
    )
    lines.append("")
    lines.append(
        f"Span precision (pack-id predictions only): "
        f"{precision['precision']:.3f} ({precision['tp']}/{precision['total']})"
    )
    lo, hi = ci["recall"]
    lines.append(f"Bootstrap 95% CI (pack ids): leak recall [{lo:.3f}, {hi:.3f}]")
    lines.append("")
    return "\n".join(lines)


def run(split: str, out_lines: list[str], runs: list[dict]) -> None:
    notes = load_notes(split)
    pack_notes = [
        {
            **note,
            "entities": [ent for ent in note["entities"] if ent["type"] in CORE_GOLD_TYPES],
        }
        for note in notes
    ]
    preds = predict_core(notes)
    stats, precision, per_note = evaluate_notes(pack_notes, preds)
    ci = bootstrap_ci(per_note)
    out_lines.append(format_table(split, stats, precision, ci))
    o = overall(stats)
    runs.append(
        {
            "system": "Core scanner",
            "split": split,
            "entities": {
                entity: {
                    "gold": s.gold,
                    "detected": s.detected,
                    "covered": s.covered,
                    "recall": s.recall,
                    "strict_recall": s.strict_recall,
                }
                for entity, s in sorted(stats.items())
            },
            "overall": o,
            "span_precision": precision,
            "bootstrap_ci_95": ci,
        }
    )
    print(
        f"Core scanner       {split}: pack-id recall={o['recall']:.3f} "
        f"strict={o['strict_recall']:.3f} fn={o['fn_rate']:.3f}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=["gold", "generated"], default="gold")
    parser.add_argument("--all", action="store_true", help="both splits")
    args = parser.parse_args()

    results_dir = REPO / "evaluation" / "results"
    results_dir.mkdir(exist_ok=True)

    metadata = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "engine": "core.scan",
        "score_threshold": DEFAULT_THRESHOLD,
    }
    out_lines = [
        "# Core scanner evaluation",
        "",
        f"Generated: {metadata['generated_at']} | engine={metadata['engine']}",
        "",
    ]
    runs: list[dict] = []

    for split in ["gold", "generated"] if args.all else [args.split]:
        run(split, out_lines, runs)

    (results_dir / "results_core.md").write_text("\n".join(out_lines), encoding="utf-8")
    (results_dir / "results_core.json").write_text(
        json.dumps({"metadata": metadata, "runs": runs}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nWrote {results_dir}/results_core.md and results_core.json")


if __name__ == "__main__":
    main()
