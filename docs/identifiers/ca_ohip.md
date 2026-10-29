# CA_OHIP — Ontario Health Number

## Authoritative sources

- Ontario Ministry of Health, *Health Card Validation Reference Manual* —
  <https://www.ontario.ca/files/2024-10/moh-health-card-validation-reference-manual-en-2024-10-10.pdf>
  (accessed 2026-07-06): every eligible Ontario resident is assigned a unique
  10-digit lifetime health number; validation includes a mod-10 edit check
  (HCV response code `10 FAILED_MOD10`).
- Ontario Ministry of Health, *Technical Specification for Health Card
  Validation (HCV) Service via Electronic Business Services* —
  <https://www.ontario.ca/files/2025-10/moh-ohip-technical-specification-health-card-validation-service-via-electronic-business-services-en-2025-10-08.pdf>
  (accessed 2026-07-06): health number schema pattern `[1-9]\d{9}`; version
  code schema pattern `[A-Z]{0,2}` — one or two letters when present (photo
  cards always carry a two-letter version code; red-and-white cards may have
  none, one, or two).

## Rule implemented

- Pattern (`core/specs.py`, `CA_OHIP`): first digit 1–9, then 4-3-3 digit
  groups separated by space, dash, dot or slash, with optional 1–2 trailing
  uppercase letters (score 0.4), or 10 contiguous digits + optional letters
  (score 0.15; the checksum alone promotes it to 1.0, so ~10% of random
  10-digit MRNs / encounter / compact phone numbers are flagged — measured in
  `evaluation/results/negatives_ca.md`). Compiled
  **case-sensitively**: version codes are uppercase on every card issue, and
  with IGNORECASE a lowercase English word following the number ("… 897 on
  file") was absorbed into the span as a bogus version code.
- Validator (`ca_ohip_valid`): `[1-9]\d{9}` plus 0–2 uppercase letters after
  separator stripping; Luhn (mod-10) checksum on the 10 digits. The version
  code is accepted but not semantically checked (it identifies the card
  issue, not the person).
- Context: shared health-card context ("health card", "hcn", …) plus
  "ohip", "ontario health".

## Known gaps

- Lowercase version codes (e.g. from case-folded OCR output) are not
  matched; the trade-off is deliberate (see pattern note above).
- Mod-10 pass ≠ issued number (the manual is explicit about this); real
  eligibility requires the ministry's HCV service.
