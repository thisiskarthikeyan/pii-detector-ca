"""Generate the Canadian false-positive stress corpus (plan item 3.1).

Every note in this corpus contains ZERO PII by construction, but is dense
with confusable non-PII numerics:

- Luhn-valid credit cards (share the Luhn checksum with SIN and OHIP);
- random 9- and 10-digit serial/order numbers (~10% of which collide with
  Luhn by chance — measuring that collision cost is the point, not a bug);
- US SSNs (out-of-jurisdiction identifier a CA deployment should not flag);
- ICD-10 codes, lab panels, vitals with units and ranges;
- facility phone numbers (non-personal switchboard lines);
- "context traps": sentences containing identifier context words
  ("health card", "SIN", "PHN") with NO identifier present, so nearby
  innocent numbers get context-boosted — the hard case for context gating.

Any pack-entity prediction on this corpus is a false positive. The corpus
is deterministic (seeded) and covered by the determinism manifest.

India note (see IMPLEMENTATION_PLAN.md): the initial pass is Canada-only;
--locale in is intentionally not implemented until Phase 4 (item 4.1).

Usage:
    python benchmark/generate_negatives.py --locale ca --n 300
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from presidio_recognizers_ca_in.validators import luhn_check_digit  # noqa: E402

HOSPITALS = [
    "Toronto General Hospital", "Foothills Medical Centre",
    "Vancouver General Hospital", "The Ottawa Hospital", "St. Boniface Hospital",
]

ICD_CODES = ["E11.9", "I10", "J45.909", "N39.0", "K21.9", "M54.5", "F41.1", "D64.9"]

LAB_LINES = [
    "Sodium {na} mmol/L, Potassium {k:.1f} mmol/L, Chloride {cl} mmol/L.",
    "Creatinine {cr} umol/L, eGFR {egfr} mL/min/1.73m2, Urea {urea:.1f} mmol/L.",
    "Hemoglobin {hgb} g/L, WBC {wbc:.1f} x10^9/L, Platelets {plt} x10^9/L.",
    "HbA1c {a1c:.1f}%, fasting glucose {glu:.1f} mmol/L.",
    "ALT {alt} U/L, AST {ast} U/L, ALP {alp} U/L, bilirubin {bili} umol/L.",
]

VITALS_LINES = [
    "BP {sys}/{dia} mmHg, HR {hr} bpm, RR {rr}, SpO2 {spo2}% on room air.",
    "Temperature {temp:.1f} C, weight {wt:.1f} kg, height {ht} cm.",
]

CONTEXT_TRAPS = [
    "Health card: pending verification with the provincial registry.",
    "SIN not provided at registration; billing to follow up.",
    "PHN to be confirmed by Alberta Health before claim submission.",
    "Patient declined to provide social insurance number for billing.",
    "OHIP eligibility check queued; health card number not on file.",
    "RAMQ coverage expired; carte soleil renewal in progress.",
]


def gen_credit_card(rng: random.Random) -> str:
    base = rng.choice(["4", "51", "52", "55"]) + "".join(
        rng.choices("0123456789", k=14)
    )
    base = base[:15]
    digits = base + luhn_check_digit(base)
    return " ".join(digits[i : i + 4] for i in range(0, 16, 4))


def gen_us_ssn(rng: random.Random) -> str:
    return f"{rng.randint(100, 899):03d}-{rng.randint(10, 99):02d}-{rng.randint(1000, 9999):04d}"


def gen_serial9(rng: random.Random) -> str:
    """9-digit lot/serial number; ~10% will be Luhn-valid by chance."""
    digits = "".join(rng.choices("0123456789", k=9))
    style = rng.choice(["compact", "spaced", "dashed"])
    if style == "compact":
        return digits
    sep = " " if style == "spaced" else "-"
    return sep.join([digits[:3], digits[3:6], digits[6:]])


def gen_order10(rng: random.Random) -> str:
    """10-digit order/requisition number; ~10% Luhn-collide with OHIP."""
    return "".join(rng.choices("0123456789", k=10))


def gen_accession(rng: random.Random) -> str:
    return f"ACC-{rng.randint(2020, 2026)}-{rng.randint(1000000, 9999999)}"


def gen_facility_phone(rng: random.Random) -> str:
    # 555-01xx is the reserved fictional exchange range.
    area = rng.choice(["403", "416", "604", "613", "204"])
    return f"({area}) 555-{rng.randint(100, 199):04d}"


def gen_lab_line(rng: random.Random) -> str:
    return rng.choice(LAB_LINES).format(
        na=rng.randint(133, 146), k=rng.uniform(3.4, 5.2), cl=rng.randint(96, 108),
        cr=rng.randint(50, 130), egfr=rng.randint(45, 110), urea=rng.uniform(2.5, 9.5),
        hgb=rng.randint(95, 165), wbc=rng.uniform(3.5, 14.0), plt=rng.randint(140, 420),
        a1c=rng.uniform(5.2, 9.8), glu=rng.uniform(4.0, 11.0),
        alt=rng.randint(10, 120), ast=rng.randint(12, 90), alp=rng.randint(40, 140),
        bili=rng.randint(4, 30),
    )


def gen_vitals_line(rng: random.Random) -> str:
    return rng.choice(VITALS_LINES).format(
        sys=rng.randint(100, 165), dia=rng.randint(55, 100), hr=rng.randint(52, 110),
        rr=rng.randint(12, 22), spo2=rng.randint(90, 100),
        temp=rng.uniform(36.1, 38.4), wt=rng.uniform(48, 118), ht=rng.randint(150, 195),
    )


def billing_note(hospital: str, rng: random.Random) -> str:
    return (
        f"{hospital} — BILLING WORKSHEET (no patient identifiers)\n\n"
        f"{rng.choice(CONTEXT_TRAPS)}\n"
        f"Requisition number: {gen_order10(rng)}\n"
        f"Payment card on file: {gen_credit_card(rng)} (expiry redacted).\n"
        f"Out-of-country coverage reference (US): SSN {gen_us_ssn(rng)}.\n"
        f"Switchboard: {gen_facility_phone(rng)}.\n"
    )


def lab_report_note(hospital: str, rng: random.Random) -> str:
    return (
        f"{hospital} — LABORATORY REPORT (identifiers withheld)\n\n"
        f"Accession: {gen_accession(rng)}\n"
        f"Analyzer lot number {gen_serial9(rng)}; QC passed.\n"
        f"{gen_lab_line(rng)}\n{gen_lab_line(rng)}\n"
        f"Coded diagnoses: {', '.join(rng.sample(ICD_CODES, 3))}.\n"
    )


def admin_note(hospital: str, rng: random.Random) -> str:
    return (
        f"{hospital} — UNIT ADMINISTRATIVE LOG\n\n"
        f"{rng.choice(CONTEXT_TRAPS)}\n"
        f"Infusion pump serial {gen_serial9(rng)} sent for calibration; "
        f"replacement device serial {gen_serial9(rng)} deployed.\n"
        f"{gen_vitals_line(rng)}\n"
        f"Supply order {gen_order10(rng)} placed with vendor; "
        f"reference {gen_accession(rng)}.\n"
    )


TEMPLATES = [billing_note, lab_report_note, admin_note]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=["ca", "in"], default="ca")
    parser.add_argument("--n", type=int, default=300)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.locale != "ca":
        sys.exit(
            "The negatives corpus is Canada-only in the initial pass "
            "(see IMPLEMENTATION_PLAN.md Phase 4, item 4.1)."
        )

    rng = random.Random(args.seed)
    out_dir = Path(__file__).parent / "data" / "negatives"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{args.locale}_negatives.jsonl"

    with open(out_path, "w", encoding="utf-8") as f:
        for i in range(args.n):
            template = TEMPLATES[i % len(TEMPLATES)]
            note = {
                "id": f"{args.locale}-neg-{i:05d}",
                "locale": args.locale,
                "note_type": template.__name__,
                "text": template(rng.choice(HOSPITALS), rng),
                "entities": [],
            }
            f.write(json.dumps(note, ensure_ascii=False) + "\n")

    print(f"Wrote {args.n} PII-free confusable notes to {out_path}")


if __name__ == "__main__":
    main()
