"""False-positive evaluation on the PII-free confusables corpus (plan 3.1).

Every note in benchmark/data/negatives/ contains zero PII, so every
pack-entity prediction (CA_* / IN_*) at or above the reporting threshold is
a false positive. Built-in Presidio entities (DATE_TIME, etc.) are out of
scope here — the pack does not own them and the corpus is not designed to
measure them.

Two configurations are compared:
- "pack (all locales)": default add_recognizers() registration;
- "pack (ca only)":     get_recognizers(["ca"]) — the registration a
  Canadian deployment should use.

Writes evaluation/results/negatives_ca.{md,json}. The FP ceiling is gated
in CI by check_thresholds.py using the "negatives_max_fp" section of
thresholds.json.

Usage:
    python benchmark/generate_negatives.py --locale ca --n 300
    python evaluation/run_negatives.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "evaluation"))

from presidio_analyzer import AnalyzerEngine  # noqa: E402
from run_eval import DEFAULT_MODEL, build_analyzer, collect_metadata  # noqa: E402

from presidio_recognizers_ca_in import get_recognizers  # noqa: E402

SCORE_THRESHOLD = 0.35
PACK_PREFIXES = ("CA_", "IN_")


def build_ca_only_analyzer(model: str = DEFAULT_MODEL) -> AnalyzerEngine:
    analyzer = build_analyzer(with_pack=False, model=model)
    for recognizer in get_recognizers(["ca"]):
        analyzer.registry.add_recognizer(recognizer)
    return analyzer


def evaluate(analyzer: AnalyzerEngine, notes: list[dict]) -> dict:
    fp_by_entity: Counter[str] = Counter()
    notes_affected = 0
    examples: dict[str, list[str]] = {}
    for note in notes:
        results = analyzer.analyze(
            text=note["text"], language="en", score_threshold=SCORE_THRESHOLD
        )
        pack_hits = [r for r in results if r.entity_type.startswith(PACK_PREFIXES)]
        if pack_hits:
            notes_affected += 1
        for r in pack_hits:
            fp_by_entity[r.entity_type] += 1
            examples.setdefault(r.entity_type, [])
            if len(examples[r.entity_type]) < 5:
                examples[r.entity_type].append(note["text"][r.start : r.end])
    return {
        "notes": len(notes),
        "fp_total": sum(fp_by_entity.values()),
        "fp_per_100_notes": round(100 * sum(fp_by_entity.values()) / len(notes), 2),
        "notes_affected": notes_affected,
        "fp_by_entity": dict(sorted(fp_by_entity.items())),
        "examples": examples,
    }


def main() -> None:
    path = REPO / "benchmark" / "data" / "negatives" / "ca_negatives.jsonl"
    if not path.exists():
        sys.exit(f"ERROR: {path} missing — run benchmark/generate_negatives.py first.")
    with open(path, encoding="utf-8") as f:
        notes = [json.loads(line) for line in f]
    assert all(not n["entities"] for n in notes), "negatives corpus must be PII-free"

    configs = {
        "pack (all locales)": build_analyzer(with_pack=True),
        "pack (ca only)": build_ca_only_analyzer(),
    }

    results = {}
    lines = [
        "# False-positive evaluation — Canadian confusables corpus",
        "",
        f"{len(notes)} PII-free notes; every CA_*/IN_* prediction at threshold "
        f">= {SCORE_THRESHOLD} is a false positive.",
        "",
    ]
    for config, analyzer in configs.items():
        r = evaluate(analyzer, notes)
        results[config] = r
        lines += [
            f"### {config}",
            "",
            f"Total pack-entity FPs: {r['fp_total']} "
            f"({r['fp_per_100_notes']} per 100 notes; "
            f"{r['notes_affected']}/{r['notes']} notes affected)",
            "",
            "| Entity | FPs | Example matches |",
            "|---|---|---|",
        ]
        for entity, count in r["fp_by_entity"].items():
            samples = "; ".join(f"`{e}`" for e in r["examples"].get(entity, []))
            lines.append(f"| {entity} | {count} | {samples} |")
        lines.append("")
        print(
            f"{config:22s}: {r['fp_total']} FPs "
            f"({r['fp_per_100_notes']}/100 notes), by entity {r['fp_by_entity']}"
        )

    out_dir = REPO / "evaluation" / "results"
    (out_dir / "negatives_ca.md").write_text("\n".join(lines), encoding="utf-8")
    (out_dir / "negatives_ca.json").write_text(
        json.dumps(
            {"metadata": collect_metadata(), "results": results},
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"\nWrote {out_dir}/negatives_ca.md and negatives_ca.json")


if __name__ == "__main__":
    main()
