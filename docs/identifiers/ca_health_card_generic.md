# CA_HEALTH_CARD — Generic provincial health card fallback

## Scope

Fallback for provinces and territories without a dedicated recognizer:
SK, MB, NS, NB, NL, PE, YT, NT, NU. Formats vary across these jurisdictions
(6–12 digits, some with letter prefixes) and none publishes a validation
algorithm. Replacing this fallback with per-province recognizers (or
documented format profiles verified against official sources) is plan
item 3.5.

## Rule implemented

- Pattern (`core/specs.py`, `CA_HEALTH_CARD`): 0–2 uppercase letters +
  6–12 digits, score **0.01** — far below the 0.35 reporting threshold, so a
  match surfaces only with context-word boosting.
- Context: single tokens, because Presidio's lemma enhancer matches one token
  at a time — "health", "card", "hcn", "phn", "medicare", "msp" (BC),
  "hsn" (SK), "phin" (MB), "mcp" (NL), and French "maladie", "assurance",
  "soleil", "ramq". (Before this list carried single tokens the recognizer
  never fired on "health card" text at all.)
- No validator: with no published structure there is nothing deterministic
  to check.
- Separated forms (`\d{3,6}[-. /]\d{3,6}`, `\d{3,4}[-. /]\d{3}[-. /]\d{3,4}`)
  are matched at the same floor score so the 5-4 Alberta rendering and
  3-3-3 / 4-3-3 renderings are covered.
- Measured (benchmark, generated split): pack recall 0.82. The misses are
  placements with no context word within Presidio's 5-token window
  (tab-separated extracts, unlabelled prose). Measured FP cost of the
  context gate on the negatives corpus: an innocent 9-digit number inside
  the window of a context word is flagged in ~70% (English), ~110%
  (French) and ~140% (Alberta, two labels) of cases.
- Attribution: a 9-digit number under generic "health card" wording is
  reported as `CA_HEALTH_CARD` only; `CA_AB_ULI` requires Alberta-specific
  context ("alberta", "uli", "ahcip", "netcare"). In the benchmark, ULI
  values are labelled under generic headers, so `CA_AB_ULI` typed-exact
  recall is 0 by design while leak recall stays 1.0 via this recognizer.

## Known gaps

- Everything: this is a context-only net, kept deliberately weak to protect
  precision. Per-province formats to verify for 3.5 include Saskatchewan
  HSN (9 digits), Manitoba PHIN (9 digits) + 6-digit registration number,
  New Brunswick Medicare (9 digits), Nova Scotia HCN (10 digits),
  NL MCP (12 digits), PEI (8 digits), and the territories — none of these
  claims is sourced yet, which is exactly why the fallback stays
  context-gated.
