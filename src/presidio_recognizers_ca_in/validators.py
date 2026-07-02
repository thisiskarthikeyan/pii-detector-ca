"""Checksum and structural validators shared across recognizers.

All functions take the raw matched string (possibly containing spaces or
dashes) and return True when the value passes the identifier's integrity
check. Deterministic validation is the precision lever of this package:
a random digit string that merely *looks* like an identifier is rejected
unless its check digit is valid.
"""

from __future__ import annotations

import re

_NON_ALNUM = re.compile(r"[^0-9A-Za-z]")


def normalize(value: str) -> str:
    """Strip separators (spaces, dashes, dots) from a matched value."""
    return _NON_ALNUM.sub("", value)


def luhn_valid(digits: str) -> bool:
    """Luhn (mod-10) checksum used by Canadian SIN and Ontario OHIP."""
    if not digits.isdigit():
        return False
    total = 0
    # Double every second digit from the right (excluding the check digit).
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


# Verhoeff tables (dihedral group D5).
_VERHOEFF_D = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
]
_VERHOEFF_P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
]


def verhoeff_valid(digits: str) -> bool:
    """Verhoeff checksum used by Aadhaar."""
    if not digits.isdigit():
        return False
    c = 0
    for i, ch in enumerate(reversed(digits)):
        c = _VERHOEFF_D[c][_VERHOEFF_P[i % 8][int(ch)]]
    return c == 0


def verhoeff_check_digit(digits: str) -> str:
    """Compute the Verhoeff check digit for a digit string (used by the corpus generator)."""
    c = 0
    for i, ch in enumerate(reversed(digits)):
        c = _VERHOEFF_D[c][_VERHOEFF_P[(i + 1) % 8][int(ch)]]
    # Find the digit that brings the checksum to 0.
    inv = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]
    return str(inv[c])


def luhn_check_digit(digits: str) -> str:
    """Compute the Luhn check digit for a digit string (used by the corpus generator)."""
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 0:  # positions shift by one once check digit is appended
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return str((10 - total % 10) % 10)


def ca_sin_valid(value: str) -> bool:
    """Canadian SIN: 9 digits, Luhn-valid, first digit not 0 or 8."""
    digits = normalize(value)
    if len(digits) != 9 or not digits.isdigit():
        return False
    if digits[0] in "08":
        return False
    return luhn_valid(digits)


def ca_ohip_valid(value: str) -> bool:
    """Ontario health number: 10 digits (Luhn-valid), optional 1-2 letter version code."""
    cleaned = normalize(value)
    m = re.fullmatch(r"(\d{10})([A-Za-z]{0,2})", cleaned)
    if not m:
        return False
    return luhn_valid(m.group(1))


_RAMQ_RE = re.compile(r"([A-Za-z]{4})(\d{2})(\d{2})(\d{2})(\d{2})")


def ca_ramq_valid(value: str) -> bool:
    """Quebec RAMQ number: 4 letters + 8 digits encoding sex-offset birth month.

    Format: LLLL YYMM DD SS where MM is 01-12 (male) or 51-62 (female)
    and DD is a plausible day of month. There is no public checksum, so
    validation is structural.
    """
    cleaned = normalize(value)
    m = _RAMQ_RE.fullmatch(cleaned)
    if not m:
        return False
    month = int(m.group(3))
    day = int(m.group(4))
    month_ok = 1 <= month <= 12 or 51 <= month <= 62
    day_ok = 1 <= day <= 31
    return month_ok and day_ok


_BC_PHN_WEIGHTS = (2, 4, 8, 5, 10, 9, 7, 3)


def ca_bc_phn_valid(value: str) -> bool:
    """BC Personal Health Number: 10 digits, starts with 9, mod-11 weighted checksum."""
    digits = normalize(value)
    if len(digits) != 10 or not digits.isdigit() or digits[0] != "9":
        return False
    total = 0
    for d, w in zip(digits[1:9], _BC_PHN_WEIGHTS, strict=True):
        total += (int(d) * w) % 11
    check = 11 - (total % 11)
    return check == int(digits[9])


def ca_ab_uli_plausible(value: str) -> bool:
    """Alberta ULI: 9 digits, no public checksum; reject trivially implausible values."""
    digits = normalize(value)
    if len(digits) != 9 or not digits.isdigit():
        return False
    return len(set(digits)) > 1  # reject e.g. 000000000 / 111111111


def in_aadhaar_valid(value: str) -> bool:
    """Aadhaar: 12 digits, first digit 2-9, Verhoeff-valid."""
    digits = normalize(value)
    if len(digits) != 12 or not digits.isdigit():
        return False
    if digits[0] in "01":
        return False
    return verhoeff_valid(digits)


# Fourth PAN character encodes holder type (P=person, C=company, ...).
_PAN_HOLDER_TYPES = set("PCFHATBLJG")
_PAN_RE = re.compile(r"[A-Z]{5}[0-9]{4}[A-Z]")


def in_pan_valid(value: str) -> bool:
    """PAN: AAAPA9999A structure with a valid holder-type fourth letter."""
    cleaned = normalize(value).upper()
    if not _PAN_RE.fullmatch(cleaned):
        return False
    return cleaned[3] in _PAN_HOLDER_TYPES


def in_abha_plausible(value: str) -> bool:
    """ABHA health account: 14 digits; no public checksum, structural check only."""
    digits = normalize(value)
    return len(digits) == 14 and digits.isdigit() and len(set(digits)) > 1


def in_mobile_valid(value: str) -> bool:
    """Indian mobile: optional +91/0 prefix then 10 digits starting 6-9."""
    digits = normalize(value)
    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]
    elif digits.startswith("0") and len(digits) == 11:
        digits = digits[1:]
    return len(digits) == 10 and digits.isdigit() and digits[0] in "6789"
