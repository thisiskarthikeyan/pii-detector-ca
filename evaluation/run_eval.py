"""Evaluation harness: stock Presidio vs. Presidio + recognizer pack.

Three systems are compared:

- "Stock Presidio": the default recognizer registry;
- "Presidio + CA builtins": stock plus Presidio's own Canadian recognizers
  (CaSinRecognizer, CaPostalCodeRecognizer) which ship disabled by default
  (added upstream in 2.2.363 / 2.2.365) — the strongest no-pack baseline;
- "Presidio + pack": stock plus this package's recognizers.

Splits:

- "heldout": the first 100 notes of the fixed-seed generator stream
  (benchmark/data/gold/ca_gold.jsonl). It has NOT been human-reviewed; the
  file path keeps the historical name, the reports do not.
- "generated": the remaining notes of the same stream.

Usage:
    python evaluation/run_eval.py --all            # heldout + generated splits
    python evaluation/run_eval.py --split heldout

Writes markdown tables, a machine-readable results.json (consumed by
check_thresholds.py in CI), and a JSON error-analysis dump to
evaluation/results/.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as pkg_version
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "evaluation"))

from metrics import PACK_PREFIX, Span, bootstrap_ci, evaluate_notes, overall  # noqa: E402
from presidio_analyzer import AnalyzerEngine  # noqa: E402
from presidio_analyzer.nlp_engine import NlpEngineProvider  # noqa: E402

from pii_detector_ca import add_recognizers  # noqa: E402

DEFAULT_MODEL = "en_core_web_sm"
SPLITS = ["heldout", "generated"]
SPLIT_PATHS = {
    "heldout": REPO / "benchmark" / "data" / "gold" / "ca_gold.jsonl",
    "generated": REPO / "benchmark" / "data" / "generated" / "ca.jsonl",
}


def collect_metadata(model: str = DEFAULT_MODEL) -> dict:
    """Environment metadata recorded with every results file (reproducibility)."""
    versions = {}
    for pkg in ["presidio-analyzer", "spacy", model]:
        try:
            versions[pkg] = pkg_version(pkg)
        except PackageNotFoundError:
            versions[pkg] = "not installed"
    metadata = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python": sys.version.split()[0],
        "versions": versions,
        "nlp_model": model,
        "score_threshold": 0.35,
    }
    manifest = REPO / "benchmark" / "data" / "checksums.json"
    if manifest.exists():
        metadata["corpus_checksums"] = json.loads(manifest.read_text(encoding="utf-8"))
    return metadata


def build_analyzer(
    with_pack: bool,
    model: str = DEFAULT_MODEL,
    *,
    presidio_ca_builtins: bool = False,
    exclude: list[str] | None = None,
) -> AnalyzerEngine:
    nlp_config = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "en", "model_name": model}],
    }
    provider = NlpEngineProvider(nlp_configuration=nlp_config)
    analyzer = AnalyzerEngine(nlp_engine=provider.create_engine(), supported_languages=["en"])
    if presidio_ca_builtins:
        for recognizer in _presidio_ca_builtins():
            analyzer.registry.add_recognizer(recognizer)
    if with_pack:
        add_recognizers(analyzer.registry, exclude=exclude or ())
    return analyzer


def _presidio_ca_builtins() -> list:
    """Presidio's own Canadian recognizers, when the installed version has them."""
    from presidio_analyzer import predefined_recognizers as pr

    found = []
    for name in ("CaSinRecognizer", "CaPostalCodeRecognizer"):
        cls = getattr(pr, name, None)
        if cls is not None:
            found.append(cls())
    return found


def predict_presidio(analyzer: AnalyzerEngine, notes: list[dict]) -> list[list[Span]]:
    predictions = []
    for note in notes:
        results = analyzer.analyze(text=note["text"], language="en", score_threshold=0.35)
        predictions.append([Span(r.start, r.end, r.entity_type) for r in results])
    return predictions


def load_notes(split: str) -> list[dict]:
    with open(SPLIT_PATHS[split], encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def _fmt_ci(ci: dict, key: str) -> str:
    if key not in ci:
        return "n/a"
    lo, hi = ci[key]
    return f"[{lo:.3f}, {hi:.3f}]"


def format_table(system: str, split: str, stats: dict, precision: dict, ci: dict) -> str:
    lines = [
        f"### {system} — split={split}",
        "",
        "| Entity | Gold | Leak recall | Strict recall | Pack recall | Typed exact |",
        "|---|---|---|---|---|---|",
    ]
    for entity in sorted(stats):
        s = stats[entity]
        lines.append(
            f"| {entity} | {s.gold} | {s.recall:.3f} | {s.strict_recall:.3f} | "
            f"{s.attributed_recall:.3f} | {s.typed_recall:.3f} |"
        )
    o = overall(stats)
    lines.append(
        f"| **TOTAL** | {o['gold']} | {o['recall']:.3f} | {o['strict_recall']:.3f} | "
        f"{o['attributed_recall']:.3f} | {o['typed_recall']:.3f} |"
    )
    pipe, pack = precision["pipeline"], precision["pack"]
    over = precision["overredaction"]
    lines += [
        "",
        "Pack recall = gold span overlapped by the recognizer that owns the entity "
        "type (CA_STREET_ADDRESS for ADDRESS, DATE_TIME for DATE); leak recall "
        "counts overlap by any recognizer.",
        "",
        f"Pipeline precision (all predictions, deduplicated): {pipe['precision']:.3f} "
        f"(TP {pipe['tp']}, FP {pipe['fp']}, duplicates on claimed gold {pipe['dup']})",
        f"Pack precision (CA_* predictions only): {pack['precision']:.3f} "
        f"(TP {pack['tp']}, FP {pack['fp']}, duplicates {pack['dup']})",
        f"Over-redaction: {over['chars_per_note']:.1f} chars/note masked outside gold spans",
        f"Bootstrap 95% CI (1000 note-resamples): leak recall {_fmt_ci(ci, 'recall')}, "
        f"strict recall {_fmt_ci(ci, 'strict_recall')}, "
        f"pack recall {_fmt_ci(ci, 'attributed_recall')}, "
        f"pipeline precision {_fmt_ci(ci, 'precision')}, "
        f"pack precision {_fmt_ci(ci, 'pack_precision')}",
        "",
    ]
    counts = precision["pred_counts"]
    if counts:
        lines += [
            "| Predicted type | TP (overlaps gold) | FP (no gold overlap) |",
            "|---|---|---|",
        ]
        for ptype, c in counts.items():
            lines.append(f"| {ptype} | {c['tp']} | {c['fp']} |")
        lines.append("")
    by_form = precision.get("by_form")
    if by_form and system == "Presidio + pack":
        lines += [
            "Per surface form (pack system only): gold entities tagged with the "
            "rendering the generator used.",
            "",
            "| Entity | Form | Gold | Leak recall | Strict recall | Pack recall |",
            "|---|---|---|---|---|---|",
        ]
        for key, s in by_form.items():
            entity, form = key.split("|", 1)
            lines.append(
                f"| {entity} | {form} | {s['gold']} | {s['recall']:.3f} | "
                f"{s['strict_recall']:.3f} | {s['attributed_recall']:.3f} |"
            )
        lines.append("")
    return "\n".join(lines)


def run(
    split: str,
    out_lines: list[str],
    errors: dict,
    runs: list[dict],
    model: str = DEFAULT_MODEL,
) -> None:
    notes = load_notes(split)
    systems = {
        "Stock Presidio": predict_presidio(build_analyzer(with_pack=False, model=model), notes),
        "Presidio + CA builtins": predict_presidio(
            build_analyzer(with_pack=False, model=model, presidio_ca_builtins=True), notes
        ),
        "Presidio + pack": predict_presidio(build_analyzer(with_pack=True, model=model), notes),
    }

    for system, preds in systems.items():
        stats, precision, per_note = evaluate_notes(notes, preds)
        ci = bootstrap_ci(per_note)
        out_lines.append(format_table(system, split, stats, precision, ci))
        errors[f"{system}|{split}"] = {
            "missed": {
                entity: s.missed_values for entity, s in stats.items() if s.missed_values
            },
            "unattributed": {
                entity: s.unattributed_values
                for entity, s in stats.items()
                if s.unattributed_values
            },
        }
        o = overall(stats)
        runs.append(
            {
                "system": system,
                "split": split,
                "nlp_model": model,
                "entities": {entity: s.as_dict() for entity, s in sorted(stats.items())},
                "overall": o,
                "span_precision": precision,
                "pack_prefix": PACK_PREFIX,
                "bootstrap_ci_95": ci,
            }
        )
        print(
            f"{system:24s} {split}: leak={o['recall']:.3f} "
            f"strict={o['strict_recall']:.3f} pack={o['attributed_recall']:.3f} "
            f"pack-precision={precision['pack']['precision']:.3f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=SPLITS, default="heldout")
    parser.add_argument("--all", action="store_true", help="both splits")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="spaCy model for the NLP engine (e.g. en_core_web_lg). Non-default "
        "models write to results_<model>.* so the canonical gated results are "
        "not overwritten.",
    )
    args = parser.parse_args()

    results_dir = REPO / "evaluation" / "results"
    results_dir.mkdir(exist_ok=True)

    metadata = collect_metadata(args.model)
    header = [
        "# Evaluation results",
        "",
        f"Generated: {metadata['generated_at']} | Python {metadata['python']} | "
        + " | ".join(f"{k} {v}" for k, v in metadata["versions"].items()),
        "",
        "The `heldout` split is the first 100 notes of the fixed-seed generator "
        "stream; it is not human-reviewed. All data is synthetic.",
        "",
    ]
    out_lines = list(header)
    errors: dict = {}
    runs: list[dict] = []
    for split in SPLITS if args.all else [args.split]:
        run(split, out_lines, errors, runs, model=args.model)

    suffix = "" if args.model == DEFAULT_MODEL else f"_{args.model}"
    (results_dir / f"results{suffix}.md").write_text("\n".join(out_lines), encoding="utf-8")
    (results_dir / f"results{suffix}.json").write_text(
        json.dumps({"metadata": metadata, "runs": runs}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (results_dir / f"error_analysis{suffix}.json").write_text(
        json.dumps(errors, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nWrote {results_dir}/results{suffix}.md, results{suffix}.json, "
          f"error_analysis{suffix}.json")


if __name__ == "__main__":
    main()
