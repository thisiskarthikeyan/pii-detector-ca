"""Generate the Canadian adversarial / hard split (plan item 3.2).

The main benchmark is circular for identifier recall: generators emit exactly
the surface forms the recognizer regexes match, so 1.000 recall is close to
tautological. This split breaks that circularity by rendering checksum-valid
identifiers in out-of-distribution surface forms. Recall here is expected to
DEGRADE; the per-variant degradation table is the honest recall number.

Each note contains exactly one identifier, tagged with its perturbation
variant so effects can be isolated against the `control` variant:

- control            standard grouping with a context label (baseline; should
                     match main-benchmark behavior)
- no_context         standard grouping, but no identifier context words
                     anywhere in the note (checksum types should still hit;
                     context-gated ULI is expected to miss by design)
- unusual_separator  dot-separated, non-standard regrouping, or slash
                     (dot and slash are matched since the separator class
                     was widened; regrouping is not)
- line_wrap          value wrapped across a newline mid-identifier
- ocr_confusable     one digit OCR-corrupted (0->O or 1->l) in the surface;
                     the gold span is the corrupted text, as a scanner would
                     see it
- dictation          every character space-separated, as dictation
                     transcripts often render numbers

Gold spans are recorded at insertion time and remain exact by construction
(including newlines and corrupted characters). Deterministic given --seed.

Usage:
    python benchmark/generate_hard.py --per-cell 50
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pii_generators import (  # noqa: E402
    raw_ca_ab_uli,
    raw_ca_bc_phn,
    raw_ca_ohip,
    raw_ca_ramq,
    raw_ca_sin,
)

VARIANTS = [
    "control",
    "no_context",
    "unusual_separator",
    "line_wrap",
    "ocr_confusable",
    "dictation",
]


# Raw checksum-valid values come from the benchmark generators, which use the
# reference checksums in checksums_ref.py (not the package validators).
_raw_sin = raw_ca_sin
_raw_ohip = raw_ca_ohip
_raw_bc_phn = raw_ca_bc_phn
_raw_ab_uli = raw_ca_ab_uli


def _raw_ramq(rng: random.Random) -> str:
    return raw_ca_ramq(rng)


@dataclass(frozen=True)
class EntitySpec:
    raw: Callable[[random.Random], str]
    groups: list[int]
    label: str


# Label lines are chosen so at least one single-token context word from the
# recognizer's context list is present (Presidio's lemma context enhancer
# matches single tokens only).
SPEC = {
    "CA_SIN": EntitySpec(_raw_sin, [3, 3, 3], "SIN:"),
    "CA_OHIP": EntitySpec(_raw_ohip, [4, 3, 3], "OHIP:"),
    "CA_RAMQ": EntitySpec(_raw_ramq, [4, 4, 4], "RAMQ:"),
    "CA_BC_PHN": EntitySpec(_raw_bc_phn, [4, 3, 3], "PHN:"),
    "CA_AB_ULI": EntitySpec(_raw_ab_uli, [5, 4], "Alberta health card ULI:"),
}


# --- Surface perturbations ----------------------------------------------------


def _group(raw: str, groups: list[int], sep: str) -> str:
    parts, i = [], 0
    for g in groups:
        parts.append(raw[i : i + g])
        i += g
    return sep.join(parts)


def _standard(raw: str, groups: list[int], rng: random.Random) -> str:
    return _group(raw, groups, rng.choice([" ", "-"]))


def _unusual_separator(raw: str, groups: list[int], rng: random.Random) -> str:
    style = rng.choice(["dot", "regroup", "slash"])
    if style == "dot":
        return _group(raw, groups, ".")
    if style == "slash":
        return _group(raw, groups, "/")
    # Non-standard regrouping, e.g. 9 digits as 2-4-3 instead of 3-3-3.
    n = len(raw)
    cut1 = rng.randint(1, n - 2)
    cut2 = rng.randint(cut1 + 1, n - 1)
    return f"{raw[:cut1]} {raw[cut1:cut2]} {raw[cut2:]}"


def _line_wrap(raw: str, groups: list[int], rng: random.Random) -> str:
    parts = _group(raw, groups, " ").split(" ")
    wrap_at = rng.randrange(len(parts) - 1)
    return (
        " ".join(parts[: wrap_at + 1]) + "\n" + " ".join(parts[wrap_at + 1 :])
    )


_OCR_MAP = {"0": "O", "1": "l"}


def _ocr_confusable(raw: str, groups: list[int], rng: random.Random) -> str:
    surface = _group(raw, groups, " ")
    positions = [i for i, ch in enumerate(surface) if ch in _OCR_MAP]
    pos = rng.choice(positions)
    return surface[:pos] + _OCR_MAP[surface[pos]] + surface[pos + 1 :]


def _dictation(raw: str, groups: list[int], rng: random.Random) -> str:
    return " ".join(raw)


RENDERERS = {
    "control": _standard,
    "no_context": _standard,
    "unusual_separator": _unusual_separator,
    "line_wrap": _line_wrap,
    "ocr_confusable": _ocr_confusable,
    "dictation": _dictation,
}

# Filler deliberately free of every context word in the CA recognizers'
# context lists, so only the label line (when present) can trigger boosting.
_NOTE_PREFIX = "OUTPATIENT PROGRESS NOTE\n\nPatient seen in clinic today.\n"
_NOTE_SUFFIX = "\nPlan: continue current management. Review in six weeks.\n"


def build_note(entity: str, variant: str, rng: random.Random) -> dict:
    spec = SPEC[entity]
    raw = spec.raw(rng)
    if variant == "ocr_confusable":
        # Guarantee an OCR-substitutable character is present.
        while not any(ch in _OCR_MAP for ch in raw):
            raw = spec.raw(rng)
    surface = RENDERERS[variant](raw, spec.groups, rng)

    if variant == "no_context":
        lead = "The intake sheet lists "
        line = f"{lead}{surface} under supplementary information."
        start_in_line = len(lead)
    else:
        lead = f"{spec.label} "
        line = lead + surface
        start_in_line = len(lead)

    text = _NOTE_PREFIX + line + _NOTE_SUFFIX
    start = len(_NOTE_PREFIX) + start_in_line
    end = start + len(surface)
    assert text[start:end] == surface
    return {
        "locale": "ca",
        "note_type": "hard",
        "variant": variant,
        "text": text,
        "entities": [
            {"start": start, "end": end, "type": entity, "value": surface}
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-cell", type=int, default=50,
                        help="notes per (entity, variant) cell")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    out_dir = Path(__file__).parent / "data" / "hard"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "ca_hard.jsonl"

    count = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for entity in SPEC:
            for variant in VARIANTS:
                for _ in range(args.per_cell):
                    note = build_note(entity, variant, rng)
                    note["id"] = f"ca-hard-{count:05d}"
                    f.write(json.dumps(note, ensure_ascii=False) + "\n")
                    count += 1

    print(
        f"Wrote {count} hard-split notes "
        f"({len(SPEC)} entities x {len(VARIANTS)} variants x {args.per_cell}) "
        f"to {out_path}"
    )


if __name__ == "__main__":
    main()
