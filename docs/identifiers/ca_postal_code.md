# CA_POSTAL_CODE — Canadian postal code

## Authoritative sources

- Canada Post, *Addressing Guidelines* —
  <https://www.canadapost-postescanada.ca/cpc/en/support/kb/sending/general-information/how-to-address-mail-and-parcels>
  (accessed 2026-07-06): postal code format is `ANA NAN` (letter-digit
  alternating, space between the forward sortation area and the local
  delivery unit).
- Letter-class rules (documented by Canada Post's addressing standards and
  uniformly reproduced): the letters **D, F, I, O, Q, U** never appear in
  any position; **W and Z** additionally never appear as the first letter.

## Rule implemented

- Pattern (`canada/postal_code.py`): first letter class
  `[ABCEGHJ-NPRSTVXY]`, subsequent letter class `[ABCEGHJ-NPRSTV-Z]`,
  optional space or dash between the two triples; score 0.5, boosted by
  address context words. No validator — the pattern is the full structural
  rule.

## Known gaps

- No lookup against issued forward sortation areas: structurally valid but
  unassigned codes (or codes in the wrong province) are accepted. This is
  by policy — Canada Post claims database rights over the postal-code file,
  so the package (and the benchmark, which generates synthetic codes only)
  must not embed real code lists.
- Lowercase postal codes ("m5g 2c4") match via Presidio's default
  IGNORECASE compilation.
