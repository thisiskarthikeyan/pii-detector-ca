# CA_RAMQ — Quebec Health Insurance Number (NAM)

## Authoritative sources

- Régie de l'assurance maladie du Québec (RAMQ), *Utilisation de la carte
  d'assurance maladie* — <https://www.ramq.gouv.qc.ca/fr/citoyens/assurance-maladie/utilisation-carte>
  (accessed 2026-07-06): the numéro d'assurance maladie (NAM) is unique and
  is the only information encoded in the card's bar code.
- RAMQ, *Manuel des pharmaciens* (billing manual distributed to Quebec
  pharmacies, 2025 edition): the NAM is a 12-character alphanumeric code.
  RAMQ's published composition (also reproduced consistently in secondary
  descriptions of the card):
  - 3 first letters of the family name at birth;
  - 1st letter of the first name;
  - last 2 digits of the year of birth;
  - month of birth, **with 50 added for women** (so 01–12 or 51–62);
  - day of birth;
  - a 2-digit administrative code used by the Régie (distinguishes people
    whose first 10 characters are identical; some descriptions call the
    final digit a "chiffre-preuve", but no checksum algorithm is published).

## Rule implemented

- Pattern (`core/specs.py`): 4 uppercase letters
  (accented allowed — CÔT, GAG) + 8 digits, optionally in 4-4-4 groups
  separated by space, dash, dot or slash (score 0.4). Matching is **case-sensitive**: with Presidio's default
  IGNORECASE, any lowercase 4-letter word followed by 8 digits ("card 4111
  1111 …") would match and be boosted by the structural validator.
- Validator (`ca_ramq_valid`): 4 letters + 8 digits after separator
  stripping; month field 01–12 or 51–62; day field 01–31. No checksum
  exists, so validation is structural only.
- Benchmark generator (`gen_ca_ramq`): builds the letter block from a
  sampled surname (3 letters, apostrophes/hyphens dropped, X-padded if
  short) + a first-name initial drawn from the census-weighted first-name
  distribution — matching RAMQ's published composition (plan item 3.6).
- Context: shared health-card context plus French terms ("assurance
  maladie", "carte soleil", "ramq").

## Known gaps

- Day is validated as 01–31 for every month; RAMQ publishes no per-month
  day rule, and tightening it (e.g. rejecting Feb 30) would add little
  precision while risking false rejections on administratively assigned
  values.
- The final two digits are accepted as any value 00–99; the "chiffre-preuve"
  algorithm, if one exists, is not public.
- The rule for surnames shorter than 3 letters (or non-Latin names) is not
  publicly documented; the generator X-pads as a synthetic convention.
- The NAM encodes name, birth date, and sex — a matched NAM is itself a
  quasi-identifier disclosure beyond the number.
