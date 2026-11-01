"""False-positive evaluation on the PII-free confusables corpus (plan 3.1).

Every note in benchmark/data/negatives/ contains zero PII, so every
pack-entity prediction (CA_*) at or above the reporting threshold is a
false positive. Each FP is attributed to the confusable value it overlaps
(the corpus records every planted number with a ``source`` tag) so the
report says WHICH kind of number causes the FPs, and CI can set a ceiling
per source instead of one blended rate. An FP that overlaps no planted
value is attributed to "unplanted".

Built-in Presidio entities (DATE_TIME, etc.) are out of scope: the pack
does not own them and the corpus is not designed to measure them.

Writes evaluation/results/negatives_ca.{md,json}.

Usage:
    python benchmark/generate_negatives.py --n 300
    python evaluation/run_negatives.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "evaluation"))

from presidio_analyzer import AnalyzerEngine  # noqa: E402
from run_eval import build_analyzer, collect_metadata  # noqa: E402

SCORE_THRESHOLD = 0.35
PACK_PREFIXES = ("CA_",)


def _source_for(r, confusables: list[dict]) -> str:
    for c in confusables:
        if r.start < c["end"] and c["start"] < r.end:
            return c["source"]
    return "unplanted"


def evaluate(analyzer: AnalyzerEngine, notes: list[dict]) -> dict:
    fp_by_entity: Counter[str] = Counter()
    fp_by_source: Counter[str] = Counter()
    planted_by_source: Counter[str] = Counter()
    fp_by_source_entity: dict[str, Counter[str]] = defaultdict(Counter)
    notes_affected = 0
    examples: dict[str, list[str]] = {}
    for note in notes:
        confusables = note.get("confusables", [])
        for c in confusables:
            planted_by_source[c["source"]] += 1
        results = analyzer.analyze(
            text=note["text"], language="en", score_threshold=SCORE_THRESHOLD
        )
        pack_hits = [r for r in results if r.entity_type.startswith(PACK_PREFIXES)]
        if pack_hits:
            notes_affected += 1
        for r in pack_hits:
            source = _source_for(r, confusables)
            fp_by_entity[r.entity_type] += 1
            fp_by_source[source] += 1
            fp_by_source_entity[source][r.entity_type] += 1
            examples.setdefault(source, [])
            if len(examples[source]) < 4:
                examples[source].append(f"{r.entity_type}: {note['text'][r.start:r.end]}")
    n = len(notes)
    return {
        "notes": n,
        "fp_total": sum(fp_by_entity.values()),
        "fp_per_100_notes": round(100 * sum(fp_by_entity.values()) / n, 2),
        "notes_affected": notes_affected,
        "fp_by_entity": dict(sorted(fp_by_entity.items())),
        "by_source": {
            source: {
                "planted": planted_by_source.get(source, 0),
                "fp": fp_by_source.get(source, 0),
                "fp_rate": (
                    round(fp_by_source.get(source, 0) / planted_by_source[source], 4)
                    if planted_by_source.get(source)
                    else None
                ),
                "fp_per_100_notes": round(100 * fp_by_source.get(source, 0) / n, 2),
                "by_entity": dict(sorted(fp_by_source_entity[source].items())),
            }
            for source in sorted(set(planted_by_source) | set(fp_by_source))
        },
        "examples": examples,
    }


def main() -> None:
    path = REPO / "benchmark" / "data" / "negatives" / "ca_negatives.jsonl"
    if not path.exists():
        sys.exit(f"ERROR: {path} missing — run benchmark/generate_negatives.py first.")
    with open(path, encoding="utf-8") as f:
        notes = [json.loads(line) for line in f]
    assert all(not n["entities"] for n in notes), "negatives corpus must be PII-free"

    configs = {"pack": build_analyzer(with_pack=True)}

    results = {}
    lines = [
        "# False-positive evaluation — Canadian confusables corpus",
        "",
        f"{len(notes)} PII-free notes; every CA_* prediction at threshold "
        f">= {SCORE_THRESHOLD} is a false positive. Each FP is attributed to the "
        "planted confusable value it overlaps (`source`); `fp_rate` is FPs per "
        "planted value of that source.",
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
            "| Source | Planted | FPs | FP rate | FP / 100 notes | By entity | Examples |",
            "|---|---|---|---|---|---|---|",
        ]
        for source, s in r["by_source"].items():
            rate = "n/a" if s["fp_rate"] is None else f"{s['fp_rate']:.3f}"
            ents = ", ".join(f"{e} {c}" for e, c in s["by_entity"].items()) or "-"
            ex = "; ".join(f"`{e}`" for e in r["examples"].get(source, [])) or "-"
            lines.append(
                f"| {source} | {s['planted']} | {s['fp']} | {rate} | "
                f"{s['fp_per_100_notes']} | {ents} | {ex} |"
            )
        lines.append("")
        print(
            f"{config:22s}: {r['fp_total']} FPs "
            f"({r['fp_per_100_notes']}/100 notes), by entity {r['fp_by_entity']}"
        )
        for source, s in r["by_source"].items():
            print(f"  {source:16s} planted={s['planted']:4d} fp={s['fp']:3d} rate={s['fp_rate']}")

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
