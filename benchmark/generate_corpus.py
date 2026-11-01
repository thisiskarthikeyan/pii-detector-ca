"""Generate the span-labeled synthetic Canadian clinical corpus.

Usage:
    python benchmark/generate_corpus.py --n 1000 --seed 42

Output: JSONL files under benchmark/data/generated/ with records:
    {"id": ..., "locale": "ca", "note_type": ..., "text": ...,
     "entities": [{"start": ..., "end": ..., "type": ..., "value": ...,
                   "form": ...}]}

``form`` records the surface rendering the generator chose for the value
(e.g. "dash", "compact+version_glued", "lowercase"); the evaluation reports
recall per form so renderings the recognizers miss are visible rather than
averaged away.

The first --gold notes of each run are written to benchmark/data/gold/ and
evaluated as the "heldout" split. They are NOT human-reviewed.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from pii_generators import (
    HOSPITALS_CA,
    RENDERERS_CA,
    gen_date,
    gen_dob,
    gen_person,
    render_address,
    render_ca_ramq,
    render_other_province_card,
)
from templates import CLINICAL_FINDINGS, DIAGNOSES, IMPRESSIONS, MEDICATIONS, TEMPLATES

CLINICAL_HISTORIES = [
    "Persistent cough for three weeks.",
    "Follow-up of known pulmonary nodule.",
    "Chronic low back pain, rule out degenerative change.",
    "Abnormal liver function tests.",
    "New-onset headache, rule out acute pathology.",
    "Right upper quadrant pain.",
    "Hematuria, rule out renal calculus.",
    "Shortness of breath on exertion, two weeks.",
    "Postoperative follow-up, day 10 after laparoscopic cholecystectomy.",
    "Recurrent urinary tract infections.",
    "Poorly controlled type 2 diabetes; medication review requested.",
    "Palpitations at rest, rule out arrhythmia.",
]

# Non-PII filler slots resolved from fixed pools.
_STATIC_POOLS = {
    "CLINICAL": CLINICAL_HISTORIES,
    "FINDINGS": CLINICAL_FINDINGS,
    "IMPRESSION": IMPRESSIONS,
    "DIAGNOSIS": DIAGNOSES,
    "MEDICATION": MEDICATIONS,
}

# Generic "Health card:" slot rotates across these. ULI-shaped values and
# other-province cards under a generic label are gold CA_HEALTH_CARD.
_GENERIC_HEALTH_IDS = ["CA_OHIP", "CA_RAMQ", "CA_BC_PHN", "CA_AB_ULI", "OTHER"]


def _health_id(rng: random.Random, ctx: dict) -> tuple[str, str, str]:
    """(surface, gold_type, form) for the generic health-card slot."""
    kind = rng.choice(_GENERIC_HEALTH_IDS)
    if kind == "CA_RAMQ":
        if "patient" in ctx:
            first, last = ctx["patient"].split(" ", 1)
            surface, form = render_ca_ramq(rng, surname=last, first_name=first)
        else:
            surface, form = render_ca_ramq(rng)
        return surface, "CA_RAMQ", form
    if kind == "OTHER":
        surface, form, _label = render_other_province_card(rng)
        return surface, "CA_HEALTH_CARD", form
    surface, form = RENDERERS_CA[kind](rng)
    gold = "CA_HEALTH_CARD" if kind == "CA_AB_ULI" else kind
    return surface, gold, f"{form}" if kind != "CA_AB_ULI" else f"uli:{form}"


def _resolve_slot(slot_type: str, rng: random.Random, ctx: dict) -> tuple[str, list[dict]]:
    """Return (text, entities) where entities carry offsets relative to text.

    ``ctx`` carries the note's patient name (first PERSON slot) so a RAMQ
    letter block matches the patient, and the first health id so a repeat
    slot can reuse it.
    """
    if slot_type in _STATIC_POOLS:
        return rng.choice(_STATIC_POOLS[slot_type]), []
    if slot_type == "PERSON":
        value = gen_person(rng)
        ctx.setdefault("patient", value)
        return value, [_ent(value, "PERSON")]
    if slot_type == "DATE":
        return _single(gen_date(rng), "DATE")
    if slot_type == "DOB":
        return _single(gen_dob(rng), "DATE")
    if slot_type == "ADDRESS":
        value, form = render_address(rng)
        return value, [_ent(value, "ADDRESS", form)]
    if slot_type == "HEALTH_ID":
        value, gold, form = _health_id(rng, ctx)
        ctx.setdefault("health_id", (value, gold, form))
        return value, [_ent(value, gold, form)]
    if slot_type == "HEALTH_ID_REPEAT":
        if "health_id" not in ctx:
            value, gold, form = _health_id(rng, ctx)
            ctx["health_id"] = (value, gold, form)
        value, gold, form = ctx["health_id"]
        return value, [_ent(value, gold, f"{form}+repeat")]
    if slot_type == "AB_ULI":
        value, form = RENDERERS_CA["CA_AB_ULI"](rng)
        return value, [_ent(value, "CA_AB_ULI", form)]
    if slot_type == "POSTAL":
        value, form = RENDERERS_CA["CA_POSTAL_CODE"](rng)
        return value, [_ent(value, "CA_POSTAL_CODE", form)]
    if slot_type == "PROV_HEALTH_LINE":
        value, form, label = render_other_province_card(rng)
        text = f"{label} {value}"
        ent = _ent(value, "CA_HEALTH_CARD", form)
        ent["start"] += len(label) + 1
        ent["end"] += len(label) + 1
        return text, [ent]
    if slot_type in RENDERERS_CA:
        value, form = RENDERERS_CA[slot_type](rng)
        return value, [_ent(value, slot_type, form)]
    raise ValueError(f"unknown slot type {slot_type}")


def _ent(value: str, gold: str, form: str | None = None) -> dict:
    ent = {"start": 0, "end": len(value), "type": gold, "value": value}
    if form:
        ent["form"] = form
    return ent


def _single(value: str, gold: str) -> tuple[str, list[dict]]:
    return value, [_ent(value, gold)]


def generate_note(rng: random.Random) -> dict:
    hospital = rng.choice(HOSPITALS_CA)
    template_fn = rng.choice(TEMPLATES)
    segments = template_fn(hospital)

    text_parts: list[str] = []
    entities: list[dict] = []
    ctx: dict = {}
    cursor = 0
    for segment in segments:
        if isinstance(segment, str):
            text_parts.append(segment)
            cursor += len(segment)
            continue
        _, slot_type = segment
        text, ents = _resolve_slot(slot_type, rng, ctx)
        text_parts.append(text)
        for ent in ents:
            entities.append({**ent, "start": cursor + ent["start"], "end": cursor + ent["end"]})
        cursor += len(text)

    return {
        "locale": "ca",
        "note_type": template_fn.__name__,
        "text": "".join(text_parts),
        "entities": entities,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=1000)
    parser.add_argument("--gold", type=int, default=100, help="size of held-out split")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    out_dir = Path(__file__).parent / "data" / "generated"
    gold_dir = Path(__file__).parent / "data" / "gold"
    out_dir.mkdir(parents=True, exist_ok=True)
    gold_dir.mkdir(parents=True, exist_ok=True)

    notes = []
    for i in range(args.n):
        note = generate_note(rng)
        note["id"] = f"ca-{i:05d}"
        # Sanity-check span integrity at generation time.
        for ent in note["entities"]:
            assert note["text"][ent["start"] : ent["end"]] == ent["value"]
        notes.append(note)

    train_path = out_dir / "ca.jsonl"
    gold_path = gold_dir / "ca_gold.jsonl"
    with open(gold_path, "w", encoding="utf-8") as f:
        for note in notes[: args.gold]:
            f.write(json.dumps(note, ensure_ascii=False) + "\n")
    with open(train_path, "w", encoding="utf-8") as f:
        for note in notes[args.gold :]:
            f.write(json.dumps(note, ensure_ascii=False) + "\n")

    n_entities = sum(len(n["entities"]) for n in notes)
    print(
        f"wrote {args.gold} held-out notes to {gold_path} "
        f"and {len(notes) - args.gold} notes to {train_path} "
        f"({n_entities} labeled entities total)"
    )


if __name__ == "__main__":
    main()
