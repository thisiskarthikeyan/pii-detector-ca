"""Curate the ODA address evaluation holdout (plan item 3.9).

Independent reservoir sample (different seed from benchmark/curate_oda.py)
for non-circular street-address evaluation. Rows are formatted into notes
by benchmark/generate_address_eval.py; they are never used by the main
benchmark address generator (which reads ca_addresses_sample.csv only).

Usage (manual, when raw ODA files are present):
    python benchmark/curate_oda_eval.py --per-province 200
"""

from __future__ import annotations

import argparse
import csv
import random
from datetime import date
from pathlib import Path

from curate_oda import FIELDS, PROVINCES, RAW_DIR, curate, sha256, usable

OUT_DIR = Path(__file__).parent / "data" / "oda"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-province", type=int, default=200)
    parser.add_argument("--seed", type=int, default=1042)
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sample: list[dict] = []
    provenance: list[str] = []

    for province, (filename, pruid) in PROVINCES.items():
        raw = RAW_DIR / filename
        if not raw.exists():
            raise SystemExit(f"ERROR: {raw} missing — place raw ODA CSVs there first.")
        rng = random.Random(f"{args.seed}:{province}")
        reservoir: list[dict] = []
        seen = 0
        with open(raw, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("pruid") != pruid or not usable(row):
                    continue
                seen += 1
                if len(reservoir) < args.per_province:
                    reservoir.append(curate(row, province))
                else:
                    j = rng.randrange(seen)
                    if j < args.per_province:
                        reservoir[j] = curate(row, province)
        sample.extend(reservoir)
        provenance.append(
            f"- `{filename}` (sha256 `{sha256(raw)}`): "
            f"{seen} usable rows, {len(reservoir)} eval-sampled"
        )
        print(f"{province}: {seen} usable -> {len(reservoir)} eval holdout")

    out_path = OUT_DIR / "ca_addresses_eval.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(sample)

    (OUT_DIR / "README_eval.md").write_text(
        "\n".join(
            [
                "# ODA address evaluation holdout",
                "",
                "Contains information licensed under the Open Government Licence - Canada.",
                "Source: Statistics Canada, **Open Database of Addresses** (ODA).",
                "",
                f"Curated {date.today().isoformat()} by `benchmark/curate_oda_eval.py` "
                f"(seed {args.seed}, {args.per_province} rows/province). Used only by",
                "`benchmark/generate_address_eval.py` — not by the main benchmark",
                "address generator.",
                "",
                "Raw inputs (gitignored):",
                "",
                *provenance,
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Wrote {len(sample)} eval holdout addresses to {out_path}")


if __name__ == "__main__":
    main()
