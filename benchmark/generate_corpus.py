"""Generate the span-labeled synthetic Canadian clinical corpus.

Usage:
    python benchmark/generate_corpus.py --n 1000 --seed 42

Output: JSONL files under benchmark/data/generated/ with records:
    {"id": ..., "locale": "ca", "note_type": ..., "text": ...,
     "entities": [{"start": ..., "end": ..., "type": ..., "value": ...}]}

The first --gold notes of each run are also written to a separate
gold split file intended for manual review before use as the test set.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from pii_generators import (
    GENERATORS_CA,
    HOSPITALS_CA,
    gen_address,
    gen_ca_ramq,
    gen_date,
    gen_dob,
    gen_person,
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

# Canadian health-card slot rotates across provincial formats.
_CA_HEALTH_IDS = ["CA_OHIP", "CA_RAMQ", "CA_BC_PHN", "CA_AB_ULI"]


def _resolve_slot(slot_type: str, rng: random.Random, ctx: dict):
    """Return (text, entity_type_or_None). None = not PII (clinical filler).

    ``ctx`` carries the note's patient name (first PERSON slot) so that a
    RAMQ number's letter block matches the patient, as on a real card.
    """
    if slot_type in _STATIC_POOLS:
        return rng.choice(_STATIC_POOLS[slot_type]), None
    if slot_type == "PERSON":
        value = gen_person(rng)
        ctx.setdefault("patient", value)
        return value, "PERSON"
    if slot_type == "DATE":
        return gen_date(rng), "DATE"
    if slot_type == "DOB":
        return gen_dob(rng), "DATE"
    if slot_type == "ADDRESS":
        return gen_address(rng), "ADDRESS"
    if slot_type == "HEALTH_ID":
        entity = rng.choice(_CA_HEALTH_IDS)
        if entity == "CA_RAMQ" and "patient" in ctx:
            first, last = ctx["patient"].split(" ", 1)
            return gen_ca_ramq(rng, surname=last, first_name=first), entity
        return GENERATORS_CA[entity](rng), entity
    return GENERATORS_CA[slot_type](rng), slot_type


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
        value, entity_type = _resolve_slot(slot_type, rng, ctx)
        text_parts.append(value)
        if entity_type is not None:
            entities.append(
                {"start": cursor, "end": cursor + len(value), "type": entity_type, "value": value}
            )
        cursor += len(value)

    return {
        "locale": "ca",
        "note_type": template_fn.__name__,
        "text": "".join(text_parts),
        "entities": entities,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=1000)
    parser.add_argument("--gold", type=int, default=100, help="size of gold split")
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
        f"wrote {args.gold} gold notes to {gold_path} "
        f"and {len(notes) - args.gold} notes to {train_path} "
        f"({n_entities} labeled entities total)"
    )


if __name__ == "__main__":
    main()
