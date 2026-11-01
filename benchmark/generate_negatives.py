"""Generate the Canadian false-positive stress corpus (plan item 3.1).

Every note in this corpus contains ZERO PII by construction, but is dense
with confusable non-PII numerics. Each confusable value is recorded with
its character span and a ``source`` tag so the evaluation can attribute
every false positive to the kind of number that caused it:

- credit_card     Luhn-valid 16-digit cards (share the checksum with SIN/OHIP)
- serial9         9-digit lot/serial numbers (~8% collide with the SIN check)
- order10         10-digit order/requisition numbers (~9% collide with OHIP)
- mrn10           10-digit medical record numbers — the most common 10-digit
                  number in a real Canadian note, with no health context
- encounter10     10-digit encounter / visit numbers
- phone_compact   10-digit phone numbers written without separators
- fax_compact     10-digit fax numbers written without separators
- us_ssn          out-of-jurisdiction identifier a CA deployment should not flag
- phone_facility  switchboard numbers in (NNN) NNN-NNNN form
- accession       ACC-YYYY-NNNNNNN accession numbers
- trap_near       an innocent number within Presidio's 5-token context
                  window of a health-card / SIN / PHN context word
- trap_alberta    the same, with Alberta-specific wording (ULI context)
- trap_french     the same, with French health-card wording
- trap_far        a context sentence with NO number nearby (the original
                  traps; kept to show the window matters)

Numbers are random digits: the checksum collision rate is the quantity being
measured, so nothing is forced valid or invalid. Any pack-entity prediction
on this corpus is a false positive. Deterministic given --seed.

Usage:
    python benchmark/generate_negatives.py --n 300
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from checksums_ref import luhn_append  # noqa: E402

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

# Context sentences with no number nearby (original traps).
TRAPS_FAR = [
    "Health card: pending verification with the provincial registry.",
    "SIN not provided at registration; billing to follow up.",
    "PHN to be confirmed by Alberta Health before claim submission.",
    "Patient declined to provide social insurance number for billing.",
    "OHIP eligibility check queued; health card number not on file.",
    "RAMQ coverage expired; carte soleil renewal in progress.",
]

# Context word within 5 tokens of the number slot ({n}).
TRAPS_NEAR = [
    "Health card pending; serial {n} noted.",
    "SIN withheld, see order {n} instead.",
    "PHN unknown; device {n} assigned.",
    "OHIP check queued, reference {n}.",
    "Health number absent; lot {n} logged.",
]
TRAPS_ALBERTA = [
    "Alberta Health ULI pending; order {n} placed.",
    "AHCIP coverage unconfirmed, requisition {n} held.",
    "Netcare lookup failed; ticket {n} opened.",
]
TRAPS_FRENCH = [
    "Numéro d'assurance maladie en attente; dossier {n} ouvert.",
    "Carte soleil expirée; commande {n} en cours.",
    "Assurance maladie non confirmée, bon {n} émis.",
]


class _Note:
    """Accumulates text while recording confusable spans with their source."""

    def __init__(self) -> None:
        self.parts: list[str] = []
        self.len = 0
        self.confusables: list[dict] = []

    def add(self, text: str) -> None:
        self.parts.append(text)
        self.len += len(text)

    def add_value(self, value: str, source: str) -> None:
        self.confusables.append(
            {"start": self.len, "end": self.len + len(value), "source": source}
        )
        self.add(value)

    def add_template(self, template: str, value: str, source: str) -> None:
        before, after = template.split("{n}")
        self.add(before)
        self.add_value(value, source)
        self.add(after)

    def text(self) -> str:
        return "".join(self.parts)


def gen_credit_card(rng: random.Random) -> str:
    base = rng.choice(["4", "51", "52", "55"]) + "".join(rng.choices("0123456789", k=14))
    digits = luhn_append(base[:15])
    return " ".join(digits[i : i + 4] for i in range(0, 16, 4))


def gen_us_ssn(rng: random.Random) -> str:
    return f"{rng.randint(100, 899):03d}-{rng.randint(10, 99):02d}-{rng.randint(1000, 9999):04d}"


def gen_serial9(rng: random.Random) -> str:
    digits = "".join(rng.choices("0123456789", k=9))
    style = rng.choice(["compact", "spaced", "dashed"])
    if style == "compact":
        return digits
    sep = " " if style == "spaced" else "-"
    return sep.join([digits[:3], digits[3:6], digits[6:]])


def gen_digits(rng: random.Random, n: int) -> str:
    return "".join(rng.choices("0123456789", k=n))


def gen_phone_compact(rng: random.Random) -> str:
    # Real Canadian area codes; exchange 555-01xx is the fictional range.
    area = rng.choice(["403", "416", "604", "613", "204", "514", "902", "306", "709"])
    return f"{area}555{rng.randint(100, 199):04d}"


def gen_accession(rng: random.Random) -> str:
    return f"ACC-{rng.randint(2020, 2026)}-{rng.randint(1000000, 9999999)}"


def gen_facility_phone(rng: random.Random) -> str:
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


def billing_note(hospital: str, rng: random.Random) -> _Note:
    n = _Note()
    n.add(f"{hospital} — BILLING WORKSHEET (no patient identifiers)\n\n")
    n.add(rng.choice(TRAPS_FAR) + "\n")
    n.add("Requisition number: ")
    n.add_value(gen_digits(rng, 10), "order10")
    n.add("\nPayment card on file: ")
    n.add_value(gen_credit_card(rng), "credit_card")
    n.add(" (expiry redacted).\nOut-of-country coverage reference (US): SSN ")
    n.add_value(gen_us_ssn(rng), "us_ssn")
    n.add(".\nSwitchboard: ")
    n.add_value(gen_facility_phone(rng), "phone_facility")
    n.add(".\n")
    return n


def lab_report_note(hospital: str, rng: random.Random) -> _Note:
    n = _Note()
    n.add(f"{hospital} — LABORATORY REPORT (identifiers withheld)\n\n")
    n.add("Accession: ")
    n.add_value(gen_accession(rng), "accession")
    n.add("\nAnalyzer lot number ")
    n.add_value(gen_serial9(rng), "serial9")
    n.add("; QC passed.\n")
    n.add(f"{gen_lab_line(rng)}\n{gen_lab_line(rng)}\n")
    n.add(f"Coded diagnoses: {', '.join(rng.sample(ICD_CODES, 3))}.\n")
    return n


def admin_note(hospital: str, rng: random.Random) -> _Note:
    n = _Note()
    n.add(f"{hospital} — UNIT ADMINISTRATIVE LOG\n\n")
    n.add(rng.choice(TRAPS_FAR) + "\n")
    n.add("Infusion pump serial ")
    n.add_value(gen_serial9(rng), "serial9")
    n.add(" sent for calibration; replacement device serial ")
    n.add_value(gen_serial9(rng), "serial9")
    n.add(" deployed.\n")
    n.add(f"{gen_vitals_line(rng)}\n")
    n.add("Supply order ")
    n.add_value(gen_digits(rng, 10), "order10")
    n.add(" placed with vendor; reference ")
    n.add_value(gen_accession(rng), "accession")
    n.add(".\n")
    return n


def registration_note(hospital: str, rng: random.Random) -> _Note:
    # The numbers that actually surround a patient record: MRN, encounter,
    # compact phone/fax. None is PII under the benchmark's definition (an
    # MRN is a facility-local key), and none carries health-card context.
    n = _Note()
    n.add(f"{hospital} — ENCOUNTER HEADER (patient identifiers removed)\n\n")
    n.add("MRN: ")
    n.add_value(gen_digits(rng, 10), "mrn10")
    n.add("   Encounter #")
    n.add_value(gen_digits(rng, 10), "encounter10")
    n.add("\nClinic tel ")
    n.add_value(gen_phone_compact(rng), "phone_compact")
    n.add(" fax ")
    n.add_value(gen_phone_compact(rng), "fax_compact")
    n.add("\n")
    n.add(f"{gen_vitals_line(rng)}\n")
    return n


def context_trap_note(hospital: str, rng: random.Random) -> _Note:
    # Context words INSIDE the enhancer's window of an innocent number.
    n = _Note()
    n.add(f"{hospital} — CLERICAL NOTE\n\n")
    n.add_template(rng.choice(TRAPS_NEAR), gen_serial9(rng), "trap_near")
    n.add("\n")
    n.add_template(rng.choice(TRAPS_ALBERTA), gen_digits(rng, 9), "trap_alberta")
    n.add("\n")
    n.add_template(rng.choice(TRAPS_FRENCH), gen_digits(rng, 9), "trap_french")
    n.add("\n")
    n.add(rng.choice(TRAPS_FAR) + "\n")
    return n


TEMPLATES = [billing_note, lab_report_note, admin_note, registration_note, context_trap_note]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=300)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    out_dir = Path(__file__).parent / "data" / "negatives"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "ca_negatives.jsonl"

    with open(out_path, "w", encoding="utf-8") as f:
        for i in range(args.n):
            template = TEMPLATES[i % len(TEMPLATES)]
            built = template(rng.choice(HOSPITALS), rng)
            text = built.text()
            for c in built.confusables:
                assert text[c["start"] : c["end"]].strip() == text[c["start"] : c["end"]]
            note = {
                "id": f"ca-neg-{i:05d}",
                "locale": "ca",
                "note_type": template.__name__,
                "text": text,
                "entities": [],
                "confusables": built.confusables,
            }
            f.write(json.dumps(note, ensure_ascii=False) + "\n")

    print(f"Wrote {args.n} PII-free confusable notes to {out_path}")


if __name__ == "__main__":
    main()
