"""Curate the committed Canadian first-name list from the StatCan census table.

Source: Statistics Canada, "First names in Canada, 2021 Census of Population",
Catalogue no. 98-505-X2021007 (released 2025-03-19), under the Statistics
Canada Open Licence. Raw CSV + metadata live in
benchmark/data/external/statcan_names/ (gitignored); this script writes a
cleaned two-column table (name, count) committed to benchmark/data/
statcan_names/ and used by the benchmark's Canadian person-name generator
for frequency-weighted sampling.

Source caveats (from the product metadata), handled here or downstream:
- Names are published unaccented and upper-case ("FRANCOIS"); we title-case
  (hyphen-aware) and the generator mixes in a small accented supplement,
  since accent handling is part of what the benchmark must exercise.
- Names with national count < 250 are excluded at source; counts are
  randomly rounded to multiples of 5/10 (fine for sampling weights).

The output is a committed SOURCE ARTIFACT (CI cannot regenerate it), so it
is intentionally absent from benchmark/data/checksums.json.

Usage (manual, when the raw file is present):
    python benchmark/curate_statcan_names.py
"""

from __future__ import annotations

import csv
import hashlib
from datetime import date
from pathlib import Path

RAW = (
    Path(__file__).parent
    / "data" / "external" / "statcan_names" / "98-505-X2021007_eng_csv_data.csv"
)
OUT_DIR = Path(__file__).parent / "data" / "statcan_names"


def title_case(name: str) -> str:
    """FRANCOIS -> Francois, JEAN-PHILIPPE -> Jean-Philippe, O'BRIEN -> O'Brien."""
    for sep in ("-", "'"):
        if sep in name:
            return sep.join(part.capitalize() for part in name.split(sep))
    return name.capitalize()


def main() -> None:
    if not RAW.exists():
        raise SystemExit(f"ERROR: {RAW} missing — place the raw StatCan CSV there.")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    with open(RAW, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["GEO_LEVEL"] != "Country":
                continue
            count = int(row["GENDER_TOTAL_COUNT"])
            rows.append({"name": title_case(row["FIRST_NAME"]), "count": count})
    rows.sort(key=lambda r: (-r["count"], r["name"]))

    out_path = OUT_DIR / "ca_first_names.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "count"])
        writer.writeheader()
        writer.writerows(rows)

    raw_hash = hashlib.sha256(RAW.read_bytes()).hexdigest()
    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# Curated StatCan census first-name list",
                "",
                "Adapted from Statistics Canada, **First names in Canada, 2021 Census",
                "of Population**, Catalogue no. 98-505-X2021007, released March 19,",
                "2025. This does not constitute an endorsement by Statistics Canada",
                "of this product.",
                "",
                f"Curated {date.today().isoformat()} by `benchmark/curate_statcan_names.py`",
                f"from raw file sha256 `{raw_hash}` ({len(rows)} names, national level).",
                "",
                "Cleaning: title-cased (hyphen/apostrophe aware); name and total",
                "count only. Source publishes names UNACCENTED and excludes names",
                "with count < 250; counts are randomly rounded to multiples of 5/10.",
                "The benchmark generator compensates for accent-stripping with a",
                "small accented supplement pool (see pii_generators.py).",
                "",
                "Aggregated frequency data — contains no personal information.",
                "This file is a committed source artifact: CI cannot regenerate it,",
                "so it is intentionally absent from benchmark/data/checksums.json.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    total = sum(r["count"] for r in rows)
    print(f"Wrote {len(rows)} names (total count {total:,}) to {out_path}")


if __name__ == "__main__":
    main()
