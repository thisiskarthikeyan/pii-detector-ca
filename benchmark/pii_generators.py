"""Generators for checksum-valid Canadian identifiers and plausible PII values.

Every generator returns (surface_text, entity_type). Identifier generators
produce values that pass this package's validators, in a randomly chosen
surface format (compact / spaced / dashed) to exercise recognizer robustness.
All values are synthetic; checksum validity does not imply the identifier
was ever issued to a real person.
"""

from __future__ import annotations

import csv
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pii_detector_ca.validators import (  # noqa: E402
    ca_bc_phn_valid,
    luhn_check_digit,
)

# --- Name pools -------------------------------------------------------------

# CA first names are sampled frequency-weighted from the committed StatCan
# 2021 Census list (benchmark/data/statcan_names/, 9k+ names — see README
# there). The census publishes names UNACCENTED, so a small accented
# supplement keeps accent handling exercised in the benchmark.
CANADIAN_FIRST_ACCENTED = [
    "Émile", "Geneviève", "Chloé", "Étienne", "Océane", "Amélie", "François",
    "Marc-André", "Hélène", "René", "Gaétan", "Aurélie", "Frédéric", "Béatrice",
]
_ACCENT_SUPPLEMENT_RATE = 0.15

# Surnames stay hand-curated (the census product covers first names only):
# Anglo, Franco, South/East/Southeast Asian, Middle Eastern, and Eastern
# European names — the population a Canadian de-id system actually serves.
CANADIAN_LAST = [
    "Tremblay", "Gagnon", "Roy", "Bouchard", "Côté", "MacDonald", "Wilson", "Taylor",
    "Lavoie", "Fortin", "Campbell", "Stewart", "Bergeron", "Morin", "Singh", "Chen",
    "Beaulieu", "Pelletier", "Gauthier", "Ouellet", "Bélanger", "Lévesque",
    "Sidhu", "Dhillon", "Gill", "Sandhu", "Wong", "Li", "Zhang", "Nguyen", "Tran", "Pham",
    "Santos", "Reyes", "Ali", "Khan", "Hassan", "Ibrahim",
    "Kowalski", "O'Brien", "McCarthy", "MacLeod", "Cardinal",
]

# Canadian street/city pools were replaced by the curated ODA sample
# (see gen_address / _oda_addresses).

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
    # MOH HCV schema: [1-9]\d{9}.
    base = rng.choice("123456789") + "".join(rng.choices("0123456789", k=8))
    digits = base + luhn_check_digit(base)
    version = rng.choice(["", "AB", "KD", "JX", "MC"])
    formatted = _fmt(digits, [4, 3, 3], rng)
    if version and " " in formatted:
        return f"{formatted} {version}"
    if version and "-" in formatted:
        return f"{formatted}-{version}"
    return formatted + version


def _ramq_letters(last: str, first: str) -> str:
    """RAMQ NAM letter block: 3 letters of the surname at birth + first-name
    initial (per RAMQ's published composition). Apostrophes/hyphens are
    dropped; surnames shorter than 3 letters are X-padded (synthetic
    convention — RAMQ does not document the short-name rule publicly)."""
    surname = "".join(c for c in last if c.isalpha())[:3].ljust(3, "X")
    return (surname + first[0]).upper()


def gen_ca_ramq(
    rng: random.Random,
    surname: str | None = None,
    first_name: str | None = None,
) -> str:
    """RAMQ NAM. When the note's patient name is known the letter block is
    derived from it (as on a real card); otherwise a name is sampled."""
    last = surname if surname is not None else rng.choice(CANADIAN_LAST)
    first = first_name if first_name is not None else gen_ca_first_name(rng)
    letters = _ramq_letters(last, first)
    yy = f"{rng.randint(1930, 2015) % 100:02d}"
    # Month of birth, +50 for women (RAMQ sex-offset encoding).
    month = rng.randint(1, 12) + rng.choice([0, 50])
    dd = f"{rng.randint(1, 28):02d}"
    # Final two digits: RAMQ administrative code (distinguishes people whose
    # first 10 characters collide).
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


# --- Common PII ---------------------------------------------------------------


_STATCAN_NAMES_PATH = (
    Path(__file__).parent / "data" / "statcan_names" / "ca_first_names.csv"
)
_STATCAN_CACHE: tuple[list[str], list[int]] | None = None


def _statcan_first_names() -> tuple[list[str], list[int]]:
    """(names, cumulative counts) for frequency-weighted sampling."""
    global _STATCAN_CACHE
    if _STATCAN_CACHE is None:
        names: list[str] = []
        cum: list[int] = []
        total = 0
        with open(_STATCAN_NAMES_PATH, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                names.append(row["name"])
                total += int(row["count"])
                cum.append(total)
        _STATCAN_CACHE = (names, cum)
    return _STATCAN_CACHE


def gen_ca_first_name(rng: random.Random) -> str:
    if rng.random() < _ACCENT_SUPPLEMENT_RATE:
        return rng.choice(CANADIAN_FIRST_ACCENTED)
    names, cum = _statcan_first_names()
    return rng.choices(names, cum_weights=cum, k=1)[0]


def gen_person(rng: random.Random) -> str:
    return f"{gen_ca_first_name(rng)} {rng.choice(CANADIAN_LAST)}"


_MONTHS = ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"]


def _format_date(rng: random.Random, y: int, m: int, d: int) -> str:
    months = _MONTHS
    style = rng.choice(["long", "slash", "iso"])
    if style == "long":
        return f"{months[m - 1]} {d}, {y}"
    if style == "slash":
        return f"{d:02d}/{m:02d}/{y}"
    return f"{y}-{m:02d}-{d:02d}"


def gen_date(rng: random.Random) -> str:
    """Encounter / exam / admission date (recent past)."""
    return _format_date(rng, rng.randint(2018, 2025), rng.randint(1, 12), rng.randint(1, 28))


def gen_dob(rng: random.Random) -> str:
    """Date of birth: a plausible patient age, never a future date."""
    return _format_date(rng, rng.randint(1930, 2015), rng.randint(1, 12), rng.randint(1, 28))


# Canadian addresses are drawn from the curated StatCan ODA sample (real,
# public civic addresses under the Open Government Licence - Canada; see
# benchmark/data/oda/README.md). Postal codes remain synthetic by policy.
_ODA_SAMPLE_PATH = Path(__file__).parent / "data" / "oda" / "ca_addresses_sample.csv"
_ODA_CACHE: list[dict] = []

# French street types precede the street name ("88, rue Lacaune").
_FRENCH_STREET_TYPES = {
    "rue", "avenue", "boulevard", "chemin", "montée", "côte", "rang",
    "place", "allée", "terrasse", "croissant", "impasse", "promenade",
}


def _oda_addresses() -> list[dict]:
    if not _ODA_CACHE:
        with open(_ODA_SAMPLE_PATH, newline="", encoding="utf-8") as f:
            _ODA_CACHE.extend(csv.DictReader(f))
    return _ODA_CACHE


def _format_ca_address(row: dict, rng: random.Random) -> str:
    muni, prov = row["municipality"], row["province"]
    postal = gen_ca_postal(rng)
    typ = row["str_type"]
    if typ and typ.lower() in _FRENCH_STREET_TYPES:
        street = f"{row['street_no']}, {typ.lower()} {row['str_name']}"
    else:
        street = " ".join(
            p for p in [row["street_no"], row["str_name"], typ, row["str_dir"]] if p
        )
    style = rng.random()
    if style < 0.08:
        return f"PO Box {rng.randint(1, 9999)}, {muni}, {prov} {postal}"
    unit = row["unit"] or (str(rng.randint(1, 90)) if style < 0.18 else "")
    if unit:
        street = f"{unit}-{street}" if rng.random() < 0.5 else f"Unit {unit}, {street}"
    return f"{street}, {muni}, {prov} {postal}"


def gen_address(rng: random.Random) -> str:
    return _format_ca_address(rng.choice(_oda_addresses()), rng)


GENERATORS_CA = {
    "CA_SIN": gen_ca_sin,
    "CA_OHIP": gen_ca_ohip,
    "CA_RAMQ": gen_ca_ramq,
    "CA_BC_PHN": gen_ca_bc_phn,
    "CA_AB_ULI": gen_ca_ab_uli,
    "CA_POSTAL_CODE": gen_ca_postal,
}
