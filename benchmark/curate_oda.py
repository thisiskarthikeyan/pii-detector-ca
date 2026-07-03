"""Curate a committed address sample from raw StatCan ODA CSVs (plan 3.3).

Source: Statistics Canada, Open Database of Addresses (ODA), released under
the Open Government Licence - Canada. Raw per-province CSVs live in
benchmark/data/external/oda/ (gitignored, several hundred MB each); this
script streams them, filters usable rows, reservoir-samples a fixed number
per province, and writes a small committed sample used by the benchmark's
Canadian address generator.

The committed sample is a SOURCE ARTIFACT, not a generated corpus file: CI
cannot regenerate it (raw ODA files are not in the repo), so it is not in
the determinism manifest. Provenance (raw-file hashes, row counts, seed) is
recorded in the README written next to the sample.

The ODA postal_code column is deliberately dropped: postal codes in the
benchmark stay synthetic (Canada Post claims rights over the postal-code
database; see IMPLEMENTATION_PLAN.md 3.3).

Usage (manual, when raw files are present):
    python benchmark/curate_oda.py --per-province 2000
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import random
from datetime import date
from pathlib import Path

RAW_DIR = Path(__file__).parent / "data" / "external" / "oda"
OUT_DIR = Path(__file__).parent / "data" / "oda"

# province code -> (raw file, ODA pruid)
PROVINCES = {
    "AB": ("ODA_AB_v1.csv", "48"),
    "ON": ("ODA_ON_v1.csv", "35"),
    "QC": ("ODA_QC_v1.csv", "24"),
}

FIELDS = ["street_no", "str_name", "str_type", "str_dir", "unit", "municipality", "province"]


def _title(value: str) -> str:
    """Title-case ALL-CAPS ODA fields (AB/ON); leave mixed case (QC) alone."""
    return value.title() if value.isupper() else value


def usable(row: dict) -> bool:
    return bool(
        row.get("street_no", "").strip()
        and row.get("str_name", "").strip()
        and (row.get("csdname", "").strip() or row.get("city", "").strip())
    )


def curate(row: dict, province: str) -> dict:
    return {
        "street_no": row["street_no"].strip(),
        "str_name": _title(row["str_name"].strip()),
        "str_type": _title(row["str_type"].strip()),
        "str_dir": row["str_dir"].strip().upper(),
        "unit": row["unit"].strip(),
        "municipality": _title(row["csdname"].strip() or row["city"].strip()),
        "province": province,
    }


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-province", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=42)
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
            f"{seen} usable rows, {len(reservoir)} sampled"
        )
        print(f"{province}: {seen} usable rows -> {len(reservoir)} sampled")

    out_path = OUT_DIR / "ca_addresses_sample.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(sample)

    readme = OUT_DIR / "README.md"
    readme.write_text(
        "\n".join(
            [
                "# Curated ODA address sample",
                "",
                "Contains information licensed under the Open Government Licence - Canada.",
                "Source: Statistics Canada, **Open Database of Addresses** (ODA).",
                "",
                "Standalone civic addresses are public, non-personal data; they become",
                "PHI only through association with a patient, which in this benchmark",
                "is entirely synthetic.",
                "",
                f"Curated {date.today().isoformat()} by `benchmark/curate_oda.py` "
                f"(seed {args.seed}, {args.per_province} rows/province, reservoir-sampled",
                "from usable rows: civic number + street name + municipality present).",
                "The ODA `postal_code` column is dropped by policy - benchmark postal",
                "codes are synthetic (see IMPLEMENTATION_PLAN.md 3.3).",
                "",
                "Raw inputs (gitignored, not redistributed here):",
                "",
                *provenance,
                "",
                "This file is a source artifact: it is committed, versioned, and NOT",
                "regenerated by CI (the raw ODA files are not available there), so it",
                "is intentionally absent from benchmark/data/checksums.json.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Wrote {len(sample)} addresses to {out_path} and provenance to {readme}")


if __name__ == "__main__":
    main()
