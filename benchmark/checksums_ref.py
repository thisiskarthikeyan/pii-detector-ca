"""Reference checksum implementations for the corpus generators and oracle tests.

This module deliberately does NOT import anything from ``pii_detector_ca``.
The benchmark used to build its identifiers with the package's own
``luhn_check_digit`` / ``ca_bc_phn_valid``, so a bug shared by generator and
validator could never show up as a recall loss. Everything here is written
from the published descriptions:

- Luhn (ISO/IEC 7812-1 Annex B): table-driven doubling, check digit found
  by trial rather than by formula.
- BC PHN: BC Ministry of Health, *Software Compliance Standards, Volume 4*
  §3.2 "PHN Check Digit Number Routine" (10 significant digits, first is 9,
  transmitted as 13 digits with leading zeros).
- RAMQ NAM: RAMQ's published composition (3 surname letters + first-name
  initial + YYMMDD with +50 on the month for women + 2 administrative
  digits), with a calendar check on the day.

``tests/test_oracle.py`` asserts the package validators agree with these on
random input and on fixed vectors.
"""

from __future__ import annotations

import calendar

_LUHN_DOUBLED = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)


def luhn_sum(digits: str) -> int:
    """Luhn weighted sum of a digit string (the check digit is the last digit)."""
    total = 0
    double = False
    for ch in reversed(digits):
        d = ord(ch) - 48
        total += _LUHN_DOUBLED[d] if double else d
        double = not double
    return total


def luhn_ok(digits: str) -> bool:
    return digits.isdigit() and len(digits) > 1 and luhn_sum(digits) % 10 == 0


def luhn_append(base: str) -> str:
    """Append the single check digit that makes ``base`` Luhn-valid (by trial)."""
    for d in "0123456789":
        if luhn_ok(base + d):
            return base + d
    raise AssertionError("Luhn must admit exactly one check digit")


def sin_ok(digits: str) -> bool:
    """9 digits, Luhn-valid, first digit 1-7 or 9 (0 unused, 8 = business numbers)."""
    return len(digits) == 9 and digits[0] in "1234567" + "9" and luhn_ok(digits)


def ohip_ok(digits: str, version: str = "") -> bool:
    """10 digits, first 1-9, Luhn-valid; version code 0-2 uppercase letters."""
    return (
        len(digits) == 10
        and digits[0] != "0"
        and luhn_ok(digits)
        and len(version) <= 2
        and all("A" <= c <= "Z" for c in version)
    )


_BC_WEIGHTS = (2, 4, 8, 5, 10, 9, 7, 3)


def bc_phn_check(base9: str) -> int | None:
    """Check digit for the 9 leading digits of a BC PHN, or None if none exists.

    Volume 4 §3.2: ignore the leading 9, multiply digits 2-9 by the weights,
    take each product mod 11, sum, take mod 11, subtract from 11. A result
    of 10 or 11 means the number is invalid (no check digit can be issued).
    """
    if len(base9) != 9 or not base9.isdigit() or base9[0] != "9":
        return None
    remainder_sum = sum((int(d) * w) % 11 for d, w in zip(base9[1:], _BC_WEIGHTS, strict=True))
    result = 11 - (remainder_sum % 11)
    return None if result in (10, 11) else result


def bc_phn_ok(digits: str) -> bool:
    """Accept the 10-digit significant form or the 13-digit zero-padded transport form."""
    if len(digits) == 13 and digits.startswith("000"):
        digits = digits[3:]
    if len(digits) != 10 or not digits.isdigit():
        return False
    check = bc_phn_check(digits[:9])
    return check is not None and check == int(digits[9])


def ramq_ok(value: str) -> bool:
    """4 letters + YY + MM (+50 for women) + DD (valid for that month) + 2 digits."""
    if len(value) != 12 or not value[:4].isalpha() or not value[4:].isdigit():
        return False
    yy, mm, dd = int(value[4:6]), int(value[6:8]), int(value[8:10])
    month = mm - 50 if mm > 50 else mm
    if not 1 <= month <= 12:
        return False
    # Two-digit year: treat as 1900s or 2000s, whichever is in the past.
    year = 2000 + yy if yy <= 26 else 1900 + yy
    return 1 <= dd <= calendar.monthrange(year, month)[1]
