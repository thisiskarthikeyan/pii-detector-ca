"""Evaluation harness: stock Presidio vs. Presidio + recognizer pack.

Three systems are compared:

- "Stock Presidio": the default recognizer registry;
- "Presidio + CA builtins": stock plus Presidio's own Canadian recognizers
  (CaSinRecognizer, CaPostalCodeRecognizer) which ship disabled by default
  (added upstream in 2.2.363 / 2.2.365) — the strongest no-pack baseline;
- "Presidio + pack": stock plus this package's recognizers.

Usage:
    python evaluation/run_eval.py --all            # gold + generated splits
    python evaluation/run_eval.py --split gold

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

from metrics import Span, bootstrap_ci, evaluate_notes, overall  # noqa: E402
from presidio_analyzer import AnalyzerEngine  # noqa: E402
from presidio_analyzer.nlp_engine import NlpEngineProvider  # noqa: E402

from pii_detector_ca import add_recognizers  # noqa: E402

DEFAULT_MODEL = "en_core_web_sm"


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
    with_pack: bool, model: str = DEFAULT_MODEL, *, presidio_ca_builtins: bool = False
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
        add_recognizers(analyzer.registry)
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
    if split == "gold":
        path = REPO / "benchmark" / "data" / "gold" / "ca_gold.jsonl"
    else:
        path = REPO / "benchmark" / "data" / "generated" / "ca.jsonl"
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def format_table(system: str, split: str, stats: dict, precision: dict, ci: dict) -> str:
    lines = [
        f"### {system} — split={split}",
        "",
        "| Entity | Gold | Detected (overlap) | Recall | Strict recall | FN rate "
        "| Typed exact recall |",
        "|---|---|---|---|---|---|---|",
    ]
    for entity in sorted(stats):
        s = stats[entity]
        lines.append(
            f"| {entity} | {s.gold} | {s.detected} | {s.recall:.3f} | "
            f"{s.strict_recall:.3f} | {s.fn_rate:.3f} | {s.typed_recall:.3f} |"
        )
    o = overall(stats)
    lines.append(
        f"| **TOTAL** | {o['gold']} | {o['detected']} | {o['recall']:.3f} | "
        f"{o['strict_recall']:.3f} | {o['fn_rate']:.3f} | {o['typed_recall']:.3f} |"
    )
    lines.append("")
    lines.append(
        f"Span precision (predicted spans overlapping any gold PII): "
        f"{precision['precision']:.3f} ({precision['tp']}/{precision['total']})"
    )

    def fmt_ci(key: str) -> str:
        lo, hi = ci[key]
        return f"[{lo:.3f}, {hi:.3f}]"

    lines.append(
        f"Bootstrap 95% CI (1000 note-resamples): leak recall {fmt_ci('recall')}, "
        f"strict recall {fmt_ci('strict_recall')}, precision {fmt_ci('precision')}"
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
            entity: s.missed_values for entity, s in stats.items() if s.missed_values
        }
        o = overall(stats)
        runs.append(
            {
                "system": system,
                "split": split,
                "nlp_model": model,
                "entities": {
                    entity: {
                        "gold": s.gold,
                        "detected": s.detected,
                        "covered": s.covered,
                        "recall": s.recall,
                        "strict_recall": s.strict_recall,
                        "typed_recall": s.typed_recall,
                    }
                    for entity, s in sorted(stats.items())
                },
                "overall": o,
                "span_precision": precision,
                "bootstrap_ci_95": ci,
            }
        )
        print(
            f"{system:24s} {split}: recall={o['recall']:.3f} "
            f"strict={o['strict_recall']:.3f} fn={o['fn_rate']:.3f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=["gold", "generated"], default="gold")
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
    ]
    out_lines = list(header)
    errors: dict = {}
    runs: list[dict] = []
    for split in ["gold", "generated"] if args.all else [args.split]:
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
