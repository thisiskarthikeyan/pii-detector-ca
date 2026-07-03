"""Generate the span-labeled synthetic clinical corpus.

Usage:
    python benchmark/generate_corpus.py --locale ca --n 1000 --seed 42
    python benchmark/generate_corpus.py --locale in --n 1000 --seed 42

Output: JSONL files under benchmark/data/generated/ with records:
    {"id": ..., "locale": ..., "note_type": ..., "text": ...,
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
    GENERATORS_IN,
    HOSPITALS_CA,
    HOSPITALS_IN,
    gen_address,
    gen_date,
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
]

# CA-only additions: the India corpus is frozen (see IMPLEMENTATION_PLAN.md),
# so new filler must not perturb the IN pool and its regeneration hashes.
CLINICAL_HISTORIES_CA = CLINICAL_HISTORIES + [
    "Shortness of breath on exertion, two weeks.",
    "Postoperative follow-up, day 10 after laparoscopic cholecystectomy.",
    "Recurrent urinary tract infections.",
    "Poorly controlled type 2 diabetes; medication review requested.",
    "Palpitations at rest, rule out arrhythmia.",
]

# Non-PII filler slots resolved from fixed pools.
_STATIC_POOLS = {
    "FINDINGS": CLINICAL_FINDINGS,
    "IMPRESSION": IMPRESSIONS,
    "DIAGNOSIS": DIAGNOSES,
    "MEDICATION": MEDICATIONS,
}

# Canadian health-card slot rotates across provincial formats.
_CA_HEALTH_IDS = ["CA_OHIP", "CA_RAMQ", "CA_BC_PHN", "CA_AB_ULI"]
# Indian "ID proof" slot rotates across national identifiers.
_IN_ID_PROOFS = ["IN_AADHAAR", "IN_VOTER_ID", "IN_PASSPORT"]


def _resolve_slot(slot_type: str, locale: str, rng: random.Random):
    """Return (text, entity_type_or_None). None = not PII (clinical filler)."""
    if slot_type == "CLINICAL":
        pool = CLINICAL_HISTORIES_CA if locale == "ca" else CLINICAL_HISTORIES
        return rng.choice(pool), None
    if slot_type in _STATIC_POOLS:
        return rng.choice(_STATIC_POOLS[slot_type]), None
    if slot_type == "PERSON":
        return gen_person(rng, locale), "PERSON"
    if slot_type == "DATE":
        return gen_date(rng), "DATE"
    if slot_type == "ADDRESS":
        return gen_address(rng, locale), "ADDRESS"
    if slot_type == "HEALTH_ID":
        entity = rng.choice(_CA_HEALTH_IDS)
        return GENERATORS_CA[entity](rng), entity
    if slot_type == "ID_PROOF":
        entity = rng.choice(_IN_ID_PROOFS)
        return GENERATORS_IN[entity](rng), entity
    generators = GENERATORS_CA if slot_type.startswith("CA_") else GENERATORS_IN
    return generators[slot_type](rng), slot_type


def generate_note(locale: str, rng: random.Random) -> dict:
    hospital = rng.choice(HOSPITALS_CA if locale == "ca" else HOSPITALS_IN)
    template_fn = rng.choice(TEMPLATES[locale])
    segments = template_fn(hospital)

    text_parts: list[str] = []
    entities: list[dict] = []
    cursor = 0
    for segment in segments:
        if isinstance(segment, str):
            text_parts.append(segment)
            cursor += len(segment)
            continue
        _, slot_type = segment
        value, entity_type = _resolve_slot(slot_type, locale, rng)
        text_parts.append(value)
        if entity_type is not None:
            entities.append(
                {"start": cursor, "end": cursor + len(value), "type": entity_type, "value": value}
            )
        cursor += len(value)

    return {
        "locale": locale,
        "note_type": template_fn.__name__,
        "text": "".join(text_parts),
        "entities": entities,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=["ca", "in"], required=True)
    parser.add_argument("--n", type=int, default=1000)
    parser.add_argument("--gold", type=int, default=100, help="size of gold split")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rng = random.Random(args.seed if args.locale == "ca" else args.seed + 1)
    out_dir = Path(__file__).parent / "data" / "generated"
    gold_dir = Path(__file__).parent / "data" / "gold"
    out_dir.mkdir(parents=True, exist_ok=True)
    gold_dir.mkdir(parents=True, exist_ok=True)

    notes = []
    for i in range(args.n):
        note = generate_note(args.locale, rng)
        note["id"] = f"{args.locale}-{i:05d}"
        # Sanity-check span integrity at generation time.
        for ent in note["entities"]:
            assert note["text"][ent["start"] : ent["end"]] == ent["value"]
        notes.append(note)

    train_path = out_dir / f"{args.locale}.jsonl"
    gold_path = gold_dir / f"{args.locale}_gold.jsonl"
    with open(gold_path, "w", encoding="utf-8") as f:
        for note in notes[: args.gold]:
            f.write(json.dumps(note, ensure_ascii=False) + "\n")
    with open(train_path, "w", encoding="utf-8") as f:
        for note in notes[args.gold :]:
            f.write(json.dumps(note, ensure_ascii=False) + "\n")

    n_entities = sum(len(n["entities"]) for n in notes)
    print(
        f"locale={args.locale}: wrote {args.gold} gold notes to {gold_path} "
        f"and {len(notes) - args.gold} notes to {train_path} "
        f"({n_entities} labeled entities total)"
    )


if __name__ == "__main__":
    main()
