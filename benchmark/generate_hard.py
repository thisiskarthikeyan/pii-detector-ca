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
- line_wrap          value wrapped across a newline mid-identifier
- ocr_confusable     one digit OCR-corrupted (0->O or 1->l) in the surface;
                     the gold span is the corrupted text, as a scanner would
                     see it
- dictation          every character space-separated, as dictation
                     transcripts often render numbers

Gold spans are recorded at insertion time and remain exact by construction
(including newlines and corrupted characters). Deterministic given --seed.

Canada-only by design; the India hard split is plan item 4.2.

Usage:
    python benchmark/generate_hard.py --per-cell 10
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from presidio_recognizers_ca_in.validators import (  # noqa: E402
    ca_bc_phn_valid,
    luhn_check_digit,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pii_generators import CANADIAN_LAST, _ramq_letters  # noqa: E402

VARIANTS = [
    "control",
    "no_context",
    "unusual_separator",
    "line_wrap",
    "ocr_confusable",
    "dictation",
]


# --- Raw (unformatted) checksum-valid values ---------------------------------


def _raw_sin(rng: random.Random) -> str:
    base = rng.choice("12345679") + "".join(rng.choices("0123456789", k=7))
    return base + luhn_check_digit(base)


def _raw_ohip(rng: random.Random) -> str:
    base = "".join(rng.choices("0123456789", k=9))
    return base + luhn_check_digit(base)


def _raw_ramq(rng: random.Random) -> str:
    # Realistic letter block: 3 surname letters + first-name initial (3.6).
    letters = _ramq_letters(rng.choice(CANADIAN_LAST), rng.choice("AEJLMS"))
    yy = f"{rng.randint(30, 99):02d}"
    month = rng.randint(1, 12) + rng.choice([0, 50])
    dd = f"{rng.randint(1, 28):02d}"
    seq = f"{rng.randint(1, 99):02d}"
    return f"{letters}{yy}{month:02d}{dd}{seq}"


def _raw_bc_phn(rng: random.Random) -> str:
    while True:
        base = "9" + "".join(rng.choices("0123456789", k=8))
        for check in "0123456789":
            if ca_bc_phn_valid(base + check):
                return base + check


def _raw_ab_uli(rng: random.Random) -> str:
    digits = "".join(rng.choices("0123456789", k=9))
    if len(set(digits)) == 1:
        digits = digits[:-1] + str((int(digits[-1]) + 1) % 10)
    return digits


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
    parser.add_argument("--per-cell", type=int, default=10,
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
