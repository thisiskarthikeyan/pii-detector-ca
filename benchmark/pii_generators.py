"""Generators for checksum-valid identifiers and locale-plausible PII values.

Every generator returns (surface_text, entity_type). Identifier generators
produce values that pass this package's validators, in a randomly chosen
surface format (compact / spaced / dashed) to exercise recognizer robustness.
All values are synthetic; checksum validity does not imply the identifier
was ever issued to a real person.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from presidio_recognizers_ca_in.validators import (  # noqa: E402
    ca_bc_phn_valid,
    luhn_check_digit,
    verhoeff_check_digit,
)

# --- Name pools -------------------------------------------------------------

INDIAN_FIRST = [
    "Priya", "Rahul", "Ananya", "Vikram", "Deepika", "Arjun", "Sneha", "Ravi",
    "Kavya", "Suresh", "Meera", "Amit", "Pooja", "Rajesh", "Divya", "Sanjay",
    "Lakshmi", "Karthik", "Nisha", "Manoj", "Aishwarya", "Ramesh", "Swati", "Anil",
]
INDIAN_LAST = [
    "Sharma", "Patel", "Reddy", "Iyer", "Gupta", "Nair", "Singh", "Rao",
    "Menon", "Verma", "Krishnan", "Desai", "Joshi", "Kulkarni", "Banerjee", "Pillai",
]
CANADIAN_FIRST = [
    "Émile", "Sophie", "Liam", "Charlotte", "Noah", "Geneviève", "William", "Olivia",
    "Jean-Philippe", "Emma", "Marc-André", "Camille", "Ethan", "Isabelle", "Lucas", "Chloé",
]
CANADIAN_LAST = [
    "Tremblay", "Gagnon", "Roy", "Bouchard", "Côté", "MacDonald", "Wilson", "Taylor",
    "Lavoie", "Fortin", "Campbell", "Stewart", "Bergeron", "Morin", "Singh", "Chen",
]

INDIAN_CITIES = [
    ("Bengaluru", "Karnataka", "560034"), ("Mumbai", "Maharashtra", "400012"),
    ("Chennai", "Tamil Nadu", "600020"), ("New Delhi", "Delhi", "110029"),
    ("Hyderabad", "Telangana", "500082"), ("Pune", "Maharashtra", "411004"),
    ("Kolkata", "West Bengal", "700017"),
]
INDIAN_STREETS = [
    "MG Road", "Brigade Road", "Linking Road", "Anna Salai", "Jubilee Hills Road No 36",
    "FC Road", "Park Street", "Sarjapur Road", "Banjara Hills",
]
CANADIAN_CITIES = [
    ("Toronto", "ON"), ("Montréal", "QC"), ("Vancouver", "BC"), ("Calgary", "AB"),
    ("Ottawa", "ON"), ("Québec City", "QC"), ("Halifax", "NS"), ("Winnipeg", "MB"),
]
CANADIAN_STREETS = [
    "Yonge Street", "Rue Sainte-Catherine", "Granville Street", "17th Avenue SW",
    "Bank Street", "Grande Allée", "Spring Garden Road", "Portage Avenue",
]

HOSPITALS_IN = [
    "Apollo Hospitals", "Fortis Healthcare", "AIIMS New Delhi", "Manipal Hospital",
    "Narayana Health City", "Tata Memorial Hospital", "CMC Vellore",
]
HOSPITALS_CA = [
    "Toronto General Hospital", "CHUM", "Vancouver General Hospital",
    "Foothills Medical Centre", "The Ottawa Hospital", "Hôpital Maisonneuve-Rosemont",
]


def _fmt(digits: str, groups: list[int], rng: random.Random) -> str:
    """Randomly render digits compact, space-separated, or dash-separated."""
    style = rng.choice(["compact", "space", "dash"])
    if style == "compact":
        return digits
    sep = " " if style == "space" else "-"
    parts, i = [], 0
    for g in groups:
        parts.append(digits[i : i + g])
        i += g
    return sep.join(parts)


# --- Canadian identifiers ----------------------------------------------------


def gen_ca_sin(rng: random.Random) -> str:
    # Leading digits 0 and 8 are not issued.
    base = rng.choice("12345679") + "".join(rng.choices("0123456789", k=7))
    digits = base + luhn_check_digit(base)
    return _fmt(digits, [3, 3, 3], rng)


def gen_ca_ohip(rng: random.Random) -> str:
    base = "".join(rng.choices("0123456789", k=9))
    digits = base + luhn_check_digit(base)
    version = rng.choice(["", "AB", "KD", "JX", "MC"])
    formatted = _fmt(digits, [4, 3, 3], rng)
    if version and " " in formatted:
        return f"{formatted} {version}"
    if version and "-" in formatted:
        return f"{formatted}-{version}"
    return formatted + version


def gen_ca_ramq(rng: random.Random) -> str:
    last = rng.choice(CANADIAN_LAST)
    letters = (last[:3] + rng.choice("ABCDEFGJLMPRST")).upper()[:4]
    letters = "".join(c for c in letters if c.isalpha()).ljust(4, "X")
    yy = f"{rng.randint(30, 99):02d}"
    month = rng.randint(1, 12) + rng.choice([0, 50])
    dd = f"{rng.randint(1, 28):02d}"
    seq = f"{rng.randint(1, 99):02d}"
    digits = f"{yy}{month:02d}{dd}{seq}"
    if rng.random() < 0.5:
        return f"{letters} {digits[:4]} {digits[4:]}"
    return letters + digits


def gen_ca_bc_phn(rng: random.Random) -> str:
    while True:
        base = "9" + "".join(rng.choices("0123456789", k=8))
        for check in "0123456789":
            if ca_bc_phn_valid(base + check):
                return _fmt(base + check, [4, 3, 3], rng)


def gen_ca_ab_uli(rng: random.Random) -> str:
    digits = "".join(rng.choices("0123456789", k=9))
    if len(set(digits)) == 1:
        digits = digits[:-1] + str((int(digits[-1]) + 1) % 10)
    return _fmt(digits, [5, 4], rng)


def gen_ca_postal(rng: random.Random) -> str:
    first = rng.choice("ABCEGHJKLMNPRSTVXY")
    letters = "ABCEGHJKLMNPRSTVWXYZ"
    code = (
        first + str(rng.randint(0, 9)) + rng.choice(letters)
        + str(rng.randint(0, 9)) + rng.choice(letters) + str(rng.randint(0, 9))
    )
    return code[:3] + " " + code[3:]


# --- Indian identifiers -------------------------------------------------------


def gen_in_aadhaar(rng: random.Random) -> str:
    base = rng.choice("23456789") + "".join(rng.choices("0123456789", k=10))
    digits = base + verhoeff_check_digit(base)
    return _fmt(digits, [4, 4, 4], rng)


def gen_in_abha(rng: random.Random) -> str:
    digits = "".join(rng.choices("0123456789", k=14))
    if len(set(digits)) == 1:
        digits = digits[:-1] + str((int(digits[-1]) + 1) % 10)
    style = rng.choice(["separated", "compact"])
    if style == "separated":
        sep = rng.choice([" ", "-"])
        return sep.join([digits[:2], digits[2:6], digits[6:10], digits[10:]])
    return digits


def gen_in_pan(rng: random.Random) -> str:
    letters = "".join(rng.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    holder = rng.choice("PCFH")
    initial = rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    last = rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return f"{letters}{holder}{initial}{rng.randint(0, 9999):04d}{last}"


def gen_in_uhid(rng: random.Random) -> str:
    prefix = rng.choice(["APL", "FRT", "AIIMS", "MH", "NH", "CMC"])
    sep = rng.choice(["-", "/", ""])
    return f"{prefix}{sep}{rng.randint(10000, 9999999999)}"


def gen_in_mobile(rng: random.Random) -> str:
    number = rng.choice("6789") + "".join(rng.choices("0123456789", k=9))
    style = rng.choice(["plain", "prefixed", "spaced"])
    if style == "prefixed":
        return f"+91 {number[:5]} {number[5:]}"
    if style == "spaced":
        return f"{number[:5]} {number[5:]}"
    return number


def gen_in_pin(rng: random.Random) -> str:
    return rng.choice([c[2] for c in INDIAN_CITIES])


def gen_in_voter_id(rng: random.Random) -> str:
    return "".join(rng.choices("ABCDEFGHJKLMNPRSTUVWXYZ", k=3)) + f"{rng.randint(0, 9999999):07d}"


def gen_in_passport(rng: random.Random) -> str:
    return rng.choice("ABCDEFGHJKLMNP") + str(rng.randint(1, 9)) + f"{rng.randint(0, 999999):06d}"


# --- Common PII ---------------------------------------------------------------


def gen_person(rng: random.Random, locale: str) -> str:
    if locale == "in":
        return f"{rng.choice(INDIAN_FIRST)} {rng.choice(INDIAN_LAST)}"
    return f"{rng.choice(CANADIAN_FIRST)} {rng.choice(CANADIAN_LAST)}"


def gen_date(rng: random.Random) -> str:
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    style = rng.choice(["long", "slash", "iso"])
    y, m, d = rng.randint(2018, 2026), rng.randint(1, 12), rng.randint(1, 28)
    if style == "long":
        return f"{months[m - 1]} {d}, {y}"
    if style == "slash":
        return f"{d:02d}/{m:02d}/{y}"
    return f"{y}-{m:02d}-{d:02d}"


def gen_address(rng: random.Random, locale: str) -> str:
    if locale == "in":
        city, state, pin = rng.choice(INDIAN_CITIES)
        return f"{rng.randint(1, 400)} {rng.choice(INDIAN_STREETS)}, {city}, {state} {pin}"
    city, prov = rng.choice(CANADIAN_CITIES)
    street = rng.choice(CANADIAN_STREETS)
    return f"{rng.randint(1, 9000)} {street}, {city}, {prov} {gen_ca_postal(rng)}"


GENERATORS_CA = {
    "CA_SIN": gen_ca_sin,
    "CA_OHIP": gen_ca_ohip,
    "CA_RAMQ": gen_ca_ramq,
    "CA_BC_PHN": gen_ca_bc_phn,
    "CA_AB_ULI": gen_ca_ab_uli,
    "CA_POSTAL_CODE": gen_ca_postal,
}
GENERATORS_IN = {
    "IN_AADHAAR": gen_in_aadhaar,
    "IN_ABHA": gen_in_abha,
    "IN_PAN": gen_in_pan,
    "IN_UHID": gen_in_uhid,
    "IN_MOBILE": gen_in_mobile,
    "IN_PIN_CODE": gen_in_pin,
    "IN_VOTER_ID": gen_in_voter_id,
    "IN_PASSPORT": gen_in_passport,
}
