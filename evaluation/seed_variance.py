"""Corpus seed-variance check: how much do results move under a different seed?

Generates fresh corpora (in memory — the committed fixed-seed corpus and its
checksum manifest are untouched) for several seeds and evaluates the
"Presidio + pack" system on each, reporting the spread of leak recall,
strict recall, and span precision per locale.

Usage:
    python evaluation/seed_variance.py                # seeds 42 101 202
    python evaluation/seed_variance.py --seeds 1 2 3 --n 500

Writes evaluation/results/seed_variance.md.
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "evaluation"))
sys.path.insert(0, str(REPO / "benchmark"))

from generate_corpus import generate_note  # noqa: E402
from metrics import evaluate_notes, overall  # noqa: E402
from run_eval import build_analyzer, predict_presidio  # noqa: E402

LOCALES = ["ca", "in"]


def generate_corpus_in_memory(locale: str, n: int, seed: int) -> list[dict]:
    # Mirror generate_corpus.main: the India stream is offset by one.
    rng = random.Random(seed if locale == "ca" else seed + 1)
    notes = []
    for i in range(n):
        note = generate_note(locale, rng)
        note["id"] = f"{locale}-seed{seed}-{i:05d}"
        notes.append(note)
    return notes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 101, 202])
    parser.add_argument("--n", type=int, default=1000, help="notes per locale per seed")
    args = parser.parse_args()

    analyzer = build_analyzer(with_pack=True)

    lines = [
        "# Seed variance (Presidio + pack)",
        "",
        f"{args.n} notes per locale per seed; seeds: {args.seeds}.",
        "",
        "| Locale | Seed | Gold entities | Leak recall | Strict recall | Precision |",
        "|---|---|---|---|---|---|",
    ]
    spreads: dict[str, dict[str, list[float]]] = {}
    for locale in LOCALES:
        spreads[locale] = {"recall": [], "strict_recall": [], "precision": []}
        for seed in args.seeds:
            notes = generate_corpus_in_memory(locale, args.n, seed)
            preds = predict_presidio(analyzer, notes)
            stats, precision, _ = evaluate_notes(notes, preds)
            o = overall(stats)
            spreads[locale]["recall"].append(o["recall"])
            spreads[locale]["strict_recall"].append(o["strict_recall"])
            spreads[locale]["precision"].append(precision["precision"])
            lines.append(
                f"| {locale} | {seed} | {o['gold']} | {o['recall']:.3f} | "
                f"{o['strict_recall']:.3f} | {precision['precision']:.3f} |"
            )
            print(
                f"{locale} seed={seed}: recall={o['recall']:.3f} "
                f"strict={o['strict_recall']:.3f} precision={precision['precision']:.3f}"
            )

    lines.append("")
    for locale in LOCALES:
        for metric, values in spreads[locale].items():
            spread = max(values) - min(values)
            lines.append(
                f"- {locale} {metric}: min {min(values):.3f}, max {max(values):.3f}, "
                f"spread {spread:.3f}"
            )

    out = REPO / "evaluation" / "results" / "seed_variance.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
