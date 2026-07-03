"""Verify the benchmark corpus regenerates bit-identically from the fixed seed.

The reproducibility claim of this project depends on the generator being
deterministic across environments. This script hashes the corpus JSONL files
and compares them against the committed manifest, so any drift (stdlib RNG
behavior change, accidental generator edit without regeneration, template
change) fails CI immediately.

Usage:
    python benchmark/check_determinism.py            # verify against manifest
    python benchmark/check_determinism.py --update   # rewrite the manifest
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
MANIFEST = DATA_DIR / "checksums.json"

CORPUS_FILES = [
    "gold/ca_gold.jsonl",
    "gold/in_gold.jsonl",
    "generated/ca.jsonl",
    "generated/in.jsonl",
    "negatives/ca_negatives.jsonl",
    "hard/ca_hard.jsonl",
    "addresses/ca_address_eval.jsonl",
]


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_checksums() -> dict[str, str]:
    checksums = {}
    for rel in CORPUS_FILES:
        path = DATA_DIR / rel
        if not path.exists():
            sys.exit(
                f"ERROR: {path} missing — run benchmark/generate_corpus.py for both "
                f"locales first (--locale ca / --locale in)."
            )
        checksums[rel] = sha256_of(path)
    return checksums


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--update", action="store_true", help="rewrite the manifest from current files"
    )
    args = parser.parse_args()

    current = compute_checksums()

    if args.update:
        MANIFEST.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {MANIFEST}")
        for rel, digest in current.items():
            print(f"  {digest}  {rel}")
        return

    if not MANIFEST.exists():
        sys.exit(f"ERROR: manifest {MANIFEST} missing — run with --update to create it.")

    expected = json.loads(MANIFEST.read_text(encoding="utf-8"))
    failures = []
    for rel in CORPUS_FILES:
        exp = expected.get(rel)
        got = current[rel]
        status = "OK" if exp == got else "MISMATCH"
        if exp != got:
            failures.append(rel)
        print(f"{status:9s} {rel}\n          expected {exp}\n          got      {got}")

    if failures:
        sys.exit(
            f"\nDeterminism check FAILED for: {', '.join(failures)}.\n"
            "If the generator changed intentionally, regenerate the corpus, re-run the "
            "evaluation, and update the manifest with --update."
        )
    print("\nDeterminism check passed: corpus regenerates bit-identically.")


if __name__ == "__main__":
    main()
