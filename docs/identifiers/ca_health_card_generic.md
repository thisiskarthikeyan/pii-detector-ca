# CA_HEALTH_CARD — Generic provincial health card fallback

## Scope

Fallback for provinces and territories without a dedicated recognizer:
SK, MB, NS, NB, NL, PE, YT, NT, NU. Formats vary across these jurisdictions
(6–12 digits, some with letter prefixes) and none publishes a validation
algorithm. Replacing this fallback with per-province recognizers (or
documented format profiles verified against official sources) is plan
item 3.5.

## Rule implemented

- Pattern (`canada/health_cards.py`, `GenericCaHealthCardRecognizer`):
  0–2 uppercase letters + 6–12 digits, score **0.01** — far below the 0.35
  reporting threshold, so a match surfaces only with strong context-word
  boosting ("health card", "medicare number", "msp", French equivalents).
- No validator: with no published structure there is nothing deterministic
  to check.

## Known gaps

- Everything: this is a context-only net, kept deliberately weak to protect
  precision. Per-province formats to verify for 3.5 include Saskatchewan
  HSN (9 digits), Manitoba PHIN (9 digits) + 6-digit registration number,
  New Brunswick Medicare (9 digits), Nova Scotia HCN (10 digits),
  NL MCP (12 digits), PEI (8 digits), and the territories — none of these
  claims is sourced yet, which is exactly why the fallback stays
  context-gated.
