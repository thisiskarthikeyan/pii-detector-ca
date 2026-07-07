# CA_BC_PHN — British Columbia Personal Health Number

## Authoritative sources

- BC Ministry of Health, *Software Compliance Standards, Volume 4 — HL7
  Message Catalog* (v3.3, 2010), §3.2 "PHN Check Digit Number Routine" —
  <https://www2.gov.bc.ca/assets/gov/health/practitioner-pro/software-development-guidelines/legacy/volume-4-hl7-message-catalog.pdf>
  (accessed 2026-07-06; marked legacy but still the published algorithm).
  The same routine appears in *Volume 3 — Technical Rules* (community
  practice and hospital editions).
- Algorithm as published: the PHN is transmitted as 13 digits with leading
  zeros; the significant part is 10 digits, first digit always 9. Ignore
  the leading 9; multiply digits 2–9 by weights **2, 4, 8, 5, 10, 9, 7, 3**,
  take each product mod 11, sum the remainders, take the sum mod 11, and
  subtract from 11. If the result is 10 or 11 the number is invalid;
  otherwise it must equal the 10th digit.

## Rule implemented

- Pattern (`canada/health_cards.py`, `BcPhnRecognizer`): `9` + 4-3-3 digit
  groups (score 0.4) or 10 contiguous digits starting with 9 (score 0.15).
- Validator (`ca_bc_phn_valid`): 10 digits after separator stripping, first
  digit 9, then exactly the published routine: `sum((d*w) % 11)` over digits
  2–9, check digit `11 - (sum % 11)` compared to digit 10. Results of 10 or
  11 can never equal a single digit, so those numbers are rejected
  implicitly, as the spec requires.
- Context: shared health-card context plus "bc services card", "care card".

## Known gaps

- The 13-digit zero-padded transport form (healthnetBC/PharmaNet) is not
  matched; clinical prose in scope renders PHNs as 10 digits.
- Checksum-valid ≠ issued; ~9% of random `9XXXXXXXXX` strings pass
  (measured on the negatives corpus).
