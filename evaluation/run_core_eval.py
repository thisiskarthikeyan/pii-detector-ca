"""Evaluate the framework-neutral core scanner (no Presidio / spaCy).

Runs the same benchmark corpora as ``run_eval.py`` but uses ``core.scan()``
for pack identifier detection only. PERSON/DATE recall from spaCy is expected
to be zero here; identifier entities should match the Presidio pattern-level
behavior exercised in tests.

Usage:
    python evaluation/run_core_eval.py --all
    python evaluation/run_core_eval.py --locale ca --split gold
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

from metrics import Span, bootstrap_ci, evaluate_notes, overall  # noqa: E402

from presidio_recognizers_ca_in.core import scan  # noqa: E402
from presidio_recognizers_ca_in.core.specs import ENTITY_IDS  # noqa: E402

DEFAULT_THRESHOLD = 0.35


def load_notes(locale: str, split: str) -> list[dict]:
    if split == "gold":
        path = REPO / "benchmark" / "data" / "gold" / f"{locale}_gold.jsonl"
    else:
        path = REPO / "benchmark" / "data" / "generated" / f"{locale}.jsonl"
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def predict_core(notes: list[dict], locale: str) -> list[list[Span]]:
    predictions: list[list[Span]] = []
    for note in notes:
        matches = scan(
            note["text"],
            locales=[locale],
            threshold=DEFAULT_THRESHOLD,
        )
        predictions.append([Span(m.start, m.end, m.entity) for m in matches])
    return predictions


def format_table(locale: str, split: str, stats: dict, precision: dict, ci: dict) -> str:
    lines = [
        f"### Core scanner — locale={locale}, split={split}",
        "",
        "Identifier entities only (framework-neutral core; no spaCy PERSON/DATE).",
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


def run(locale: str, split: str, out_lines: list[str], runs: list[dict]) -> None:
    notes = load_notes(locale, split)
    pack_notes = [
        {
            **note,
            "entities": [ent for ent in note["entities"] if ent["type"] in ENTITY_IDS],
        }
        for note in notes
    ]
    preds = predict_core(notes, locale)
    pack_preds = [[span for span in spans if span.type in ENTITY_IDS] for spans in preds]
    stats, precision, per_note = evaluate_notes(pack_notes, pack_preds)
    ci = bootstrap_ci(per_note)
    out_lines.append(format_table(locale, split, stats, precision, ci))
    o = overall(stats)
    runs.append(
        {
            "system": "Core scanner",
            "locale": locale,
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
        f"Core scanner       {locale}/{split}: pack-id recall={o['recall']:.3f} "
        f"strict={o['strict_recall']:.3f} fn={o['fn_rate']:.3f}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=["ca", "in"])
    parser.add_argument("--split", choices=["gold", "generated"], default="gold")
    parser.add_argument("--all", action="store_true")
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

    if args.all:
        for locale in ["ca", "in"]:
            for split in ["gold", "generated"]:
                run(locale, split, out_lines, runs)
    else:
        if not args.locale:
            parser.error("--locale required unless --all")
        run(args.locale, args.split, out_lines, runs)

    (results_dir / "results_core.md").write_text("\n".join(out_lines), encoding="utf-8")
    (results_dir / "results_core.json").write_text(
        json.dumps({"metadata": metadata, "runs": runs}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nWrote {results_dir}/results_core.md and results_core.json")


if __name__ == "__main__":
    main()
