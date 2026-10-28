"""Checksum and structural validators for Canadian identifiers.

Framework-neutral: no Presidio or spaCy dependency. Used by the generic
``core.scanner`` and by Presidio adapters.
"""

from __future__ import annotations

import re

_NON_ALNUM = re.compile(r"[^0-9A-Za-zÀ-ÖØ-öø-ÿ]")


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
    """Ontario health number: 10 digits (Luhn-valid), optional 1-2 letter version code.

    The MOH HCV schema requires a non-zero first digit (``[1-9]\\d{9}``); the
    version code is uppercase on every card issue, so lowercase letters are
    not accepted as part of the identifier (see docs/identifiers/ca_ohip.md).
    """
    cleaned = normalize(value)
    m = re.fullmatch(r"([1-9]\d{9})([A-Z]{0,2})", cleaned)
    if not m:
        return False
    return luhn_valid(m.group(1))


# RAMQ letter block may contain accented characters from French surnames (CÔTÉ, GAGNÉ).
_RAMQ_RE = re.compile(r"([A-Za-zÀ-ÖØ-öø-ÿ]{4})(\d{2})(\d{2})(\d{2})(\d{2})")


def ca_ramq_valid(value: str) -> bool:
    """Quebec health insurance number (NAM): 4 letters + 8 digits.

    Composition per RAMQ: first 3 letters of the surname at birth, first
    letter of the first name, then YY MM DD of birth (50 is added to MM for
    women) and a 2-digit administrative code. So MM is 01-12 or 51-62 and
    DD is a day of month (validated as 01-31; RAMQ does not publish a
    per-month day rule). There is no public checksum, so validation is
    structural. See docs/identifiers/ca_ramq.md for provenance.
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


def ca_ab_uli_plausible(value: str) -> bool | None:
    """Alberta ULI plausibility: 9 digits, no public checksum.

    Returns False to reject trivially implausible values (wrong shape,
    repeated single digit such as 000000000) and None otherwise. Never
    returns True: without a checksum there is no integrity evidence, so the
    match must keep its low pattern score and rely on context-word boosting.
    """
    digits = normalize(value)
    if len(digits) != 9 or not digits.isdigit():
        return False
    if len(set(digits)) == 1:
        return False
    return None


_CA_PROVINCES = frozenset(
    {"AB", "BC", "MB", "NB", "NL", "NS", "NT", "NU", "ON", "PE", "QC", "SK", "YT"}
)
_POSTAL_TAIL = re.compile(
    r",\s*([A-Za-z]{2})\s+"
    r"([ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?"
    r"\d[ABCEGHJ-NPRSTV-Z]\d)\s*$",
    re.IGNORECASE,
)
_POSTAL_BODY = re.compile(
    r"^[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z]\d[ABCEGHJ-NPRSTV-Z]\d$"
)


def ca_street_address_valid(value: str) -> bool:
    """Structural check for a full Canadian civic address string."""
    text = value.strip()
    m = _POSTAL_TAIL.search(text)
    if not m or m.group(1).upper() not in _CA_PROVINCES:
        return False
    postal = normalize(m.group(2)).upper()
    if not _POSTAL_BODY.fullmatch(postal):
        return False
    head = text[: m.start()].strip()
    if re.match(r"^PO Box \d", head, re.IGNORECASE):
        return True
    if re.match(r"^(?:Unit \d+, )?(?:\d{1,6}-\d{1,6}|\d{1,6})", head):
        return True
    if re.match(r"^\d{1,6},", head):
        return True
    return False
