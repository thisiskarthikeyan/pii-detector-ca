# CA_STREET_ADDRESS — Canadian civic address

## Authoritative sources

Civic addresses are not a specified identifier; the recognizer encodes
Canadian addressing conventions rather than a government format rule:

- Canada Post, *Addressing Guidelines* (civic format: civic number, street
  name, street type, optional direction and unit; municipality; two-letter
  province code; postal code) — accessed 2026-07-06.
- French civic style (street type preceding the name after the civic
  number: "88, rue Lacaune") per Canada Post's French addressing
  guidelines.
- Evaluated non-circularly against real civic addresses from Statistics
  Canada's Open Database of Addresses (ODA, Open Government Licence –
  Canada); see `benchmark/data/oda/README_eval.md` and plan item 3.9.

## Rule implemented

- Patterns (`canada/street_address.py`): full address lines anchored on the
  right by `, <municipality>, <province code> <postal code>`; English form
  (civic number or `Unit N,`/`N-M` prefix or `PO Box N`) and French form
  (`N, <type français> <nom>`); score 0.55.
- Validator (`ca_street_address_valid`): re-checks province code against
  the 13 real codes, postal-code letter classes, and a plausible head
  (PO box, unit, or civic number).
- Entity type maps to gold `ADDRESS` in the evaluation harness.

## Known gaps

- Requires the full one-line form ending in province + postal code;
  addresses split across lines, missing the postal code, or written
  city-first are not matched (spaCy's built-in LOCATION covers parts of
  those — measured as the leak/strict gap in `results/address_ca.md`).
- Municipality names containing commas or newlines break the anchor.
- Rural route / general delivery styles (RR 2, GD) are not matched.
- Measured strict recall on the ODA holdout: 0.950 (gated at ≥ 0.90 in CI).
