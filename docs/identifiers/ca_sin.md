# CA_SIN — Canadian Social Insurance Number

## Authoritative sources

- Employment and Social Development Canada / Service Canada, *Social
  Insurance Number* program pages — <https://www.canada.ca/en/employment-social-development/services/sin.html>
  (accessed 2026-07-06): the SIN is a unique 9-digit number; SINs beginning
  with 9 are issued to temporary residents and expire with the holder's
  immigration documents.
- Service Canada, *The Social Insurance Number Code of Practice* —
  <https://www.canada.ca/en/employment-social-development/services/sin/reports/code-of-practice.html>
  (accessed 2026-07-06).
- The mod-10 (Luhn) check digit is not described in Service Canada's public
  program pages but is the validation applied by CRA-facing payroll and
  government systems and is uniformly documented in third-party
  implementations. Historically the first digit encoded the region of
  registration (1 Atlantic, 2–3 Quebec, 4–5 Ontario, 6 Prairies/NWT/NU,
  7 BC/Yukon, 9 temporary residents); 0 and 8 are not issued to individuals
  (8 is reserved for CRA business numbers).

## Rule implemented

- Pattern (`core/specs.py`, `CA_SIN`): 3-3-3 digit groups separated by space or dash
  (score 0.4), or 9 contiguous digits (score 0.1, needs checksum + context).
- Validator (`ca_sin_valid` in `core/validators.py`): exactly 9 digits after
  separator stripping, first digit not 0 or 8, Luhn (mod-10) checksum valid.
- Context words: "sin", "social insurance", "social insurance number",
  "numéro d'assurance sociale", "nas".

## Upstream equivalent

Presidio ≥ 2.2.363 ships `CaSinRecognizer` (`CA_SIN`, Luhn, English/French
context), disabled by default. This package's recognizer adds the first-digit
exclusion (0/8) and shares the entity name; enable one or the other
(`add_recognizers(registry, exclude=["CA_SIN"])`).

## Known gaps

- The Luhn requirement and first-digit exclusions are implemented from
  consistent secondary documentation; Service Canada does not publish a
  formal validation spec. A checksum-valid value is not evidence the SIN
  was ever issued.
- Any Luhn-valid 9-digit string with an eligible first digit is accepted;
  ~8% of random 9-digit strings collide (measured: 7.85% over 20,000 random strings).
- Region semantics of the first digit are not used for validation.
