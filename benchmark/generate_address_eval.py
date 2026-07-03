"""Generate the Canadian street-address evaluation corpus (plan item 3.9).

Each note contains one real ODA address (from the eval holdout CSV, never
used by the main benchmark generator) with an address context label.
Gold spans are exact by construction.

Usage:
    python benchmark/curate_oda_eval.py --per-province 200
    python benchmark/generate_address_eval.py --n 300
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pii_generators import _format_ca_address  # noqa: E402

EVAL_CSV = Path(__file__).parent / "data" / "oda" / "ca_addresses_eval.csv"
LABELS = [
    "Home address:",
    "Mailing address:",
    "Patient resides at",
    "Address on file:",
]

_PREFIX = "OUTPATIENT CLINIC NOTE\n\n"
_SUFFIX = "\n\nPlan: follow up in two weeks.\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=300)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if not EVAL_CSV.exists():
        sys.exit(f"ERROR: {EVAL_CSV} missing — run benchmark/curate_oda_eval.py first.")

    rows = list(csv.DictReader(open(EVAL_CSV, encoding="utf-8")))
    rng = random.Random(args.seed)
    out_dir = Path(__file__).parent / "data" / "addresses"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "ca_address_eval.jsonl"

    with open(out_path, "w", encoding="utf-8") as f:
        for i in range(args.n):
            row = rng.choice(rows)
            address = _format_ca_address(row, rng)
            label = rng.choice(LABELS)
            if label.endswith(":"):
                line = f"{label} {address}"
                start = len(_PREFIX) + len(label) + 1
            else:
                line = f"{label} {address}."
                start = len(_PREFIX) + len(label) + 1
            text = _PREFIX + line + _SUFFIX
            end = start + len(address)
            assert text[start:end] == address
            note = {
                "id": f"ca-addr-{i:05d}",
                "locale": "ca",
                "note_type": "address_eval",
                "text": text,
                "entities": [
                    {"start": start, "end": end, "type": "ADDRESS", "value": address}
                ],
            }
            f.write(json.dumps(note, ensure_ascii=False) + "\n")

    print(f"Wrote {args.n} address-eval notes to {out_path}")


if __name__ == "__main__":
    main()
